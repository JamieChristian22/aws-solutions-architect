import aws_cdk as cdk
from aws_cdk import (
    Stack, Duration, RemovalPolicy,
    aws_iot as iot,
    aws_kinesis as kinesis,
    aws_kinesisfirehose as firehose,
    aws_kinesisfirehose_destinations as destinations,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_s3 as s3,
    aws_kms as kms,
    aws_iam as iam,
    aws_sns as sns,
    aws_ec2 as ec2,
    aws_opensearchservice as opensearch,
    aws_secretsmanager as secrets,
    aws_glue as glue,
    aws_athena as athena,
    aws_cloudwatch as cw,
    aws_cognito as cognito,
)
from constructs import Construct

class IotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC for analytics / OpenSearch
        vpc = ec2.Vpc(self, "IotVpc",
            ip_addresses=ec2.IpAddresses.cidr("10.40.0.0/16"),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),
            ],
        )

        # KMS key for data-at-rest
        data_key = kms.Key(self, "IotDataKey",
            alias="alias/iot-telemetry-data",
            enable_key_rotation=True
        )

        # Buckets
        telemetry_bucket = s3.Bucket(self, "TelemetryRaw",
            bucket_name=None,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=data_key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            lifecycle_rules=[s3.LifecycleRule(expiration=Duration.days(365))],
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Kinesis stream for real-time telemetry
        kinesis_stream = kinesis.Stream(self, "SensorTelemetryStream",
            shard_count=1,
            encryption=kinesis.StreamEncryption.KMS,
            encryption_key=data_key,
            retention_period=Duration.hours(24)
        )

        # Firehose delivery stream to S3 (curated parquet-ready landing)
        fh_role = iam.Role(self, "FirehoseRole",
            assumed_by=iam.ServicePrincipal("firehose.amazonaws.com")
        )
        telemetry_bucket.grant_read_write(fh_role)
        data_key.grant_encrypt_decrypt(fh_role)

        delivery_stream = firehose.DeliveryStream(self, "TelemetryFirehose",
            destinations=[
                destinations.S3Bucket(telemetry_bucket,
                    buffering_interval=Duration.seconds(60),
                    data_output_prefix="year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/",
                    error_output_prefix="errors/!{firehose:error-output-type}/",
                    compression=destinations.Compression.GZIP,
                    logging=True,
                    role=fh_role
                )
            ],
        )

        # SNS Topic for anomaly alerts
        alert_topic = sns.Topic(self, "AlertTopic")

        # Cognito + OpenSearch for dashboards (private in VPC)
        user_pool = cognito.UserPool(self, "DashUserPool",
            self_sign_up_enabled=False,
            sign_in_aliases=cognito.SignInAliases(email=True)
        )
        user_pool_client = user_pool.add_client("DashUserPoolClient",
            auth_flows=cognito.AuthFlow(user_srp=True)
        )
        identity_pool = cognito.CfnIdentityPool(self, "DashIdentityPool",
            allow_unauthenticated_identities=False,
            cognito_identity_providers=[cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                client_id=user_pool_client.user_pool_client_id,
                provider_name=user_pool.user_pool_provider_name
            )]
        )

        os_sg = ec2.SecurityGroup(self, "OpenSearchSG", vpc=vpc, allow_all_outbound=True)
        for subnet in vpc.private_subnets:
            os_sg.add_ingress_rule(
                ec2.Peer.ipv4(subnet.ipv4_cidr_block),
                ec2.Port.tcp(443),
                "Private subnets to OpenSearch"
            )

        os_master_secret = secrets.Secret(self, "OSMasterSecret",
            generate_secret_string=secrets.SecretStringGenerator(
                secret_string_template='{"username":"master-user"}',
                generate_string_key="password"
            )
        )

        domain = opensearch.Domain(self, "TelemetrySearch",
            version=opensearch.EngineVersion.OPENSEARCH_2_13,
            vpc=vpc,
            vpc_subnets=[ec2.SubnetSelection(subnets=vpc.private_subnets)],
            security_groups=[os_sg],
            capacity=opensearch.CapacityConfig(
                data_nodes=2,
                data_node_instance_type="t3.small.search"
            ),
            ebs=opensearch.EbsOptions(
                volume_size=20
            ),
            node_to_node_encryption=True,
            encryption_at_rest=opensearch.EncryptionAtRestOptions(enabled=True),
            enforce_https=True,
            fine_grained_access_control=opensearch.AdvancedSecurityOptions(
                master_user_name="master-user",
                master_user_password=os_master_secret.secret_value_from_json("password"),
            ),
            cognito_dashboards_auth=opensearch.CognitoOptions(
                identity_pool_id=identity_pool.ref,
                user_pool_id=user_pool.user_pool_id,
                user_pool_client_id=user_pool_client.user_pool_client_id
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Stream Processor Lambda (Kinesis -> anomaly detect -> SNS + OpenSearch + Firehose)
        processor_fn = _lambda.Function(self, "TelemetryStreamProcessor",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=_lambda.Code.from_asset("../lambda/stream_processor"),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=vpc.private_subnets),
            memory_size=512,
            timeout=Duration.seconds(30),
            log_retention=logs.RetentionDays.ONE_WEEK,
            environment={
                "FIREHOSE_NAME": delivery_stream.delivery_stream_name,
                "SNS_TOPIC_ARN": alert_topic.topic_arn,
                "OS_ENDPOINT": domain.domain_endpoint,
                "OS_INDEX": "iot-telemetry",
                "OS_SECRET_ARN": os_master_secret.secret_arn,
                "TEMP_MAX_C": "80",
                "VIB_MAX_G": "5.0",
                "BATTERY_MIN_PCT": "10",
            }
        )

        # permissions
        kinesis_stream.grant_read(processor_fn)
        delivery_stream.grant_put_records(processor_fn)
        alert_topic.grant_publish(processor_fn)
        os_master_secret.grant_read(processor_fn)

        processor_fn.add_event_source_mapping("KinesisSource",
            event_source_arn=kinesis_stream.stream_arn,
            batch_size=100,
            starting_position=_lambda.StartingPosition.LATEST,
            bisect_batch_on_error=True
        )

        # Glue + Crawler + Athena Workgroup
        db = glue.CfnDatabase(self, "TelemetryDb",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(name="iot_telemetry")
        )

        crawler_role = iam.Role(self, "TelemetryCrawlerRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com")
        )
        crawler_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
        )
        telemetry_bucket.grant_read(crawler_role)

        glue.CfnCrawler(self, "TelemetryCrawler",
            role=crawler_role.role_arn,
            database_name=db.ref,
            name="iot-telemetry-crawler",
            targets=glue.CfnCrawler.TargetsProperty(
                s3_targets=[glue.CfnCrawler.S3TargetProperty(
                    path=f"s3://{telemetry_bucket.bucket_name}/"
                )]
            ),
            schema_change_policy=glue.CfnCrawler.SchemaChangePolicyProperty(
                delete_behavior="LOG",
                update_behavior="UPDATE_IN_DATABASE"
            )
        )

        results_bucket = s3.Bucket(self, "AthenaResults",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            lifecycle_rules=[s3.LifecycleRule(expiration=Duration.days(90))],
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        athena.CfnWorkGroup(self, "TelemetryWG",
            name="iot-wg",
            state="ENABLED",
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                enforce_work_group_configuration=True,
                result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                    output_location=f"s3://{results_bucket.bucket_name}/results/"
                ),
                publish_cloud_watch_metrics_enabled=True
            )
        )

        # CloudWatch Dashboard + basic alarms
        dashboard = cw.Dashboard(self, "IotDashboard",
            dashboard_name="iot-sensor-analytics"
        )

        lambda_err_metric = cw.Metric(
            namespace="AWS/Lambda",
            metric_name="Errors",
            dimensions_map={"FunctionName": processor_fn.function_name},
            statistic="Sum",
            period=Duration.minutes(5)
        )
        lambda_dur_metric = cw.Metric(
            namespace="AWS/Lambda",
            metric_name="Duration",
            dimensions_map={"FunctionName": processor_fn.function_name},
            statistic="p95",
            period=Duration.minutes(5)
        )
        kinesis_age_metric = cw.Metric(
            namespace="AWS/Kinesis",
            metric_name="GetRecords.IteratorAgeMilliseconds",
            dimensions_map={"StreamName": kinesis_stream.stream_name},
            statistic="Average",
            period=Duration.minutes(5)
        )

        dashboard.add_widgets(
            cw.GraphWidget(
                title="Processor Lambda Errors / p95 Duration",
                left=[lambda_err_metric, lambda_dur_metric]
            ),
            cw.GraphWidget(
                title="Kinesis Iterator Age (ms)",
                left=[kinesis_age_metric]
            )
        )

        cw.Alarm(self, "ProcessorErrorsAlarm",
            metric=lambda_err_metric,
            threshold=1,
            evaluation_periods=1
        )

        cw.Alarm(self, "KinesisIteratorAgeAlarm",
            metric=kinesis_age_metric,
            threshold=60000,
            evaluation_periods=1
        )

        # Outputs
        cdk.CfnOutput(self, "IotTopicPattern", value="factory/+/sensor/#")
        cdk.CfnOutput(self, "KinesisStreamName", value=kinesis_stream.stream_name)
        cdk.CfnOutput(self, "TelemetryBucketName", value=telemetry_bucket.bucket_name)
        cdk.CfnOutput(self, "AlertTopicArn", value=alert_topic.topic_arn)
        cdk.CfnOutput(self, "OpenSearchEndpoint", value=domain.domain_endpoint)
        cdk.CfnOutput(self, "AthenaWorkgroupName", value="iot-wg")
