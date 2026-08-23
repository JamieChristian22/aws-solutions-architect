from aws_cdk import (
    Stack, Duration, RemovalPolicy, CfnOutput,
    aws_apigateway as apigw,
    aws_cloudwatch as cw,
    aws_ec2 as ec2,
    aws_firehose as firehose,
    aws_glue as glue,
    aws_iam as iam,
    aws_kinesis as kinesis,
    aws_kms as kms,
    aws_lambda as _lambda,
    aws_lambda_event_sources as event_sources,
    aws_logs as logs,
    aws_opensearchservice as opensearch,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_sqs as sqs,
    aws_wafv2 as wafv2,
)
from constructs import Construct
from pathlib import Path

class ClickstreamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        key = kms.Key(self, "DataKey", enable_key_rotation=True)

        vpc = ec2.Vpc(
            self, "AnalyticsVpc",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),
            ],
        )

        stream = kinesis.Stream(
            self, "EventStream",
            stream_mode=kinesis.StreamMode.ON_DEMAND,
            encryption=kinesis.StreamEncryption.KMS,
            encryption_key=key,
            retention_period=Duration.hours(48),
        )

        lake = s3.Bucket(
            self, "ProcessedLake",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            enforce_ssl=True,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="curated-retention",
                    enabled=True,
                    transitions=[s3.Transition(storage_class=s3.StorageClass.INFREQUENT_ACCESS, transition_after=Duration.days(30))],
                    expiration=Duration.days(395),
                )
            ],
            removal_policy=RemovalPolicy.RETAIN,
        )

        error_bucket = s3.Bucket(
            self, "ErrorBucket",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            lifecycle_rules=[s3.LifecycleRule(expiration=Duration.days(30))],
            removal_policy=RemovalPolicy.RETAIN,
        )

        dlq = sqs.Queue(
            self, "ProcessorDlq",
            encryption=sqs.QueueEncryption.KMS,
            encryption_master_key=key,
            retention_period=Duration.days(14),
        )

        # Glue catalog/table for Parquet lake.
        database = glue.CfnDatabase(
            self, "GlueDatabase",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(name="clickstream"),
        )

        table = glue.CfnTable(
            self, "GlueTable",
            catalog_id=self.account,
            database_name="clickstream",
            table_input=glue.CfnTable.TableInputProperty(
                name="events",
                table_type="EXTERNAL_TABLE",
                parameters={"classification":"parquet"},
                partition_keys=[
                    glue.CfnTable.ColumnProperty(name="event_date", type="string"),
                    glue.CfnTable.ColumnProperty(name="event_hour", type="string"),
                ],
                storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                    location=f"s3://{lake.bucket_name}/events/",
                    input_format="org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                    output_format="org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                    serde_info=glue.CfnTable.SerdeInfoProperty(
                        serialization_library="org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
                    ),
                    columns=[
                        glue.CfnTable.ColumnProperty(name="event_id",type="string"),
                        glue.CfnTable.ColumnProperty(name="event_time",type="timestamp"),
                        glue.CfnTable.ColumnProperty(name="session_id",type="string"),
                        glue.CfnTable.ColumnProperty(name="anonymous_id",type="string"),
                        glue.CfnTable.ColumnProperty(name="user_id",type="string"),
                        glue.CfnTable.ColumnProperty(name="event_type",type="string"),
                        glue.CfnTable.ColumnProperty(name="page_url",type="string"),
                        glue.CfnTable.ColumnProperty(name="device_type",type="string"),
                        glue.CfnTable.ColumnProperty(name="source",type="string"),
                        glue.CfnTable.ColumnProperty(name="revenue",type="double"),
                    ],
                ),
            ),
        )
        table.add_dependency(database)

        firehose_role = iam.Role(
            self, "FirehoseRole",
            assumed_by=iam.ServicePrincipal("firehose.amazonaws.com"),
        )
        lake.grant_read_write(firehose_role)
        error_bucket.grant_read_write(firehose_role)
        key.grant_encrypt_decrypt(firehose_role)

        delivery = firehose.CfnDeliveryStream(
            self, "DeliveryStream",
            delivery_stream_type="DirectPut",
            extended_s3_destination_configuration=firehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty(
                bucket_arn=lake.bucket_arn,
                role_arn=firehose_role.role_arn,
                prefix="events/event_date=!{timestamp:yyyy-MM-dd}/event_hour=!{timestamp:HH}/",
                error_output_prefix="errors/!{firehose:error-output-type}/",
                buffering_hints=firehose.CfnDeliveryStream.BufferingHintsProperty(interval_in_seconds=300,size_in_m_bs=64),
                compression_format="GZIP",
                encryption_configuration=firehose.CfnDeliveryStream.EncryptionConfigurationProperty(
                    kms_encryption_config=firehose.CfnDeliveryStream.KMSEncryptionConfigProperty(awskms_key_arn=key.key_arn)
                ),
            ),
        )

        ingest = _lambda.Function(
            self, "IngestFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("../lambda/ingest"),
            timeout=Duration.seconds(10),
            memory_size=256,
            environment={"STREAM_NAME": stream.stream_name},
            log_retention=logs.RetentionDays.ONE_MONTH,
        )
        stream.grant_write(ingest)

        domain = opensearch.Domain(
            self, "SearchDomain",
            version=opensearch.EngineVersion.OPENSEARCH_2_13,
            vpc=vpc,
            vpc_subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],
            capacity=opensearch.CapacityConfig(data_nodes=2, data_node_instance_type="t3.small.search"),
            ebs=opensearch.EbsOptions(enabled=True, volume_size=50),
            node_to_node_encryption=True,
            encryption_at_rest=opensearch.EncryptionAtRestOptions(enabled=True,kms_key=key),
            enforce_https=True,
            zone_awareness=opensearch.ZoneAwarenessConfig(enabled=True,availability_zone_count=2),
            removal_policy=RemovalPolicy.RETAIN,
        )

        processor = _lambda.Function(
            self, "ProcessorFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("../lambda/processor"),
            timeout=Duration.seconds(60),
            memory_size=1024,
            environment={
                "DELIVERY_STREAM": delivery.ref,
                "OS_HOST": domain.domain_endpoint,
                "OS_INDEX": "clickstream-events",
            },
            vpc=vpc,
            log_retention=logs.RetentionDays.ONE_MONTH,
            dead_letter_queue=dlq,
        )
        processor.add_event_source(
            event_sources.KinesisEventSource(
                stream,
                starting_position=_lambda.StartingPosition.LATEST,
                batch_size=200,
                bisect_batch_on_error=True,
                retry_attempts=5,
                parallelization_factor=2,
                report_batch_item_failures=True,
            )
        )
        processor.add_to_role_policy(iam.PolicyStatement(
            actions=["firehose:PutRecord","firehose:PutRecordBatch"],
            resources=[delivery.attr_arn],
        ))
        domain.grant_write(processor)
        key.grant_encrypt_decrypt(processor)

        api = apigw.RestApi(
            self, "EventApi",
            deploy_options=apigw.StageOptions(
                stage_name="prod",
                throttling_rate_limit=6000,
                throttling_burst_limit=10000,
                metrics_enabled=True,
                logging_level=apigw.MethodLoggingLevel.ERROR,
            ),
        )
        events_resource = api.root.add_resource("events")
        events_resource.add_method("POST", apigw.LambdaIntegration(ingest))

        web_acl = wafv2.CfnWebACL(
            self, "WebAcl",
            scope="REGIONAL",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="clickstream-web-acl",
                sampled_requests_enabled=True,
            ),
            rules=[
                wafv2.CfnWebACL.RuleProperty(
                    name="AWSManagedCommon",
                    priority=0,
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            name="AWSManagedRulesCommonRuleSet",
                            vendor_name="AWS",
                        )
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="common-rules",
                        sampled_requests_enabled=True,
                    ),
                ),
                wafv2.CfnWebACL.RuleProperty(
                    name="RateLimit",
                    priority=1,
                    action=wafv2.CfnWebACL.RuleActionProperty(block={}),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(limit=12000,aggregate_key_type="IP")
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="rate-limit",
                        sampled_requests_enabled=True,
                    ),
                ),
            ],
        )

        wafv2.CfnWebACLAssociation(
            self, "ApiWafAssociation",
            resource_arn=f"arn:aws:apigateway:{self.region}::/restapis/{api.rest_api_id}/stages/prod",
            web_acl_arn=web_acl.attr_arn,
        )

        cw.Alarm(
            self, "IteratorAgeAlarm",
            metric=stream.metric_get_records_iterator_age_milliseconds(period=Duration.minutes(1)),
            threshold=60000,
            evaluation_periods=3,
        )
        cw.Alarm(
            self, "ProcessorErrorsAlarm",
            metric=processor.metric_errors(period=Duration.minutes(5)),
            threshold=5,
            evaluation_periods=2,
        )

        CfnOutput(self, "ApiUrl", value=api.url_for_path("/events"))
        CfnOutput(self, "KinesisStreamName", value=stream.stream_name)
        CfnOutput(self, "ProcessedBucketName", value=lake.bucket_name)
        CfnOutput(self, "OpenSearchEndpoint", value=domain.domain_endpoint)
