import aws_cdk as cdk
from aws_cdk import (
    Stack, Duration, RemovalPolicy,
    aws_kms as kms,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_wafv2 as wafv2,
    aws_kinesis as kinesis,
    aws_iam as iam,
    aws_kinesisfirehose as firehose,
    aws_kinesisfirehose_destinations as destinations,
    aws_logs as logs,
    aws_ec2 as ec2,
    aws_glue as glue,
    aws_athena as athena,
    aws_opensearchservice as opensearch,
    aws_secretsmanager as secrets,
    aws_cognito as cognito
)
from constructs import Construct

class ClickstreamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC with endpoints
        vpc = ec2.Vpc(self, "Vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.20.0.0/16"),
            nat_gateways=1, max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24)
            ]
        )
        vpc.add_gateway_endpoint("S3Endpoint", service=ec2.GatewayVpcEndpointAwsService.S3)
        for i, svc in enumerate([
            ec2.InterfaceVpcEndpointAwsService.KINESIS_STREAMS,
            ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS,
            ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH,
            ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_EVENTS,
            ec2.InterfaceVpcEndpointAwsService.STS,
            ec2.InterfaceVpcEndpointAwsService.KINESIS_FIREHOSE,
        ]):
            vpc.add_interface_endpoint(f"Endpoint{i}", service=svc, subnets=ec2.SubnetSelection(subnets=vpc.private_subnets))

        # KMS
        data_key = kms.Key(self, "DataKey", alias="alias/clickstream-data", enable_key_rotation=True)

        # S3 Buckets
        processed = s3.Bucket(self, "Processed",
            encryption=s3.BucketEncryption.KMS, encryption_key=data_key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL, enforce_ssl=True,
            lifecycle_rules=[s3.LifecycleRule(expiration=Duration.days(365))],
            auto_delete_objects=True, removal_policy=RemovalPolicy.DESTROY
        )
        bad = s3.Bucket(self, "Bad",
            encryption=s3.BucketEncryption.KMS, encryption_key=data_key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL, enforce_ssl=True,
            lifecycle_rules=[s3.LifecycleRule(expiration=Duration.days(30))],
            auto_delete_objects=True, removal_policy=RemovalPolicy.DESTROY
        )

        # Kinesis
        stream = kinesis.Stream(self, "EventStream",
            shard_count=1, stream_mode=kinesis.StreamMode.PROVISIONED,
            encryption=kinesis.StreamEncryption.KMS, encryption_key=data_key,
            retention_period=Duration.hours(24)
        )

        # Ingest Lambda (public)
        ingest = _lambda.Function(self, "IngestFn",
            runtime=_lambda.Runtime.PYTHON_3_11, handler="index.handler",
            code=_lambda.Code.from_asset("../lambda/ingest"),
            memory_size=256, timeout=Duration.seconds(10),
            environment={"STREAM_NAME": stream.stream_name, "BAD_BUCKET": bad.bucket_name, "ALLOW_ORIGINS":"https://localhost,https://example.com"},
            log_retention=logs.RetentionDays.ONE_WEEK
        )
        stream.grant_write(ingest); bad.grant_write(ingest)

        # API Gateway + WAF
        api = apigw.RestApi(self, "Api", deploy_options=apigw.StageOptions(stage_name="prod", logging_level=apigw.MethodLoggingLevel.INFO))
        api.root.add_resource("events").add_method("POST", apigw.LambdaIntegration(ingest), api_key_required=False)
        web_acl = wafv2.CfnWebACL(self, "ApiWaf",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            scope="REGIONAL", name="clickstream-api-waf",
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True, metric_name="api-waf", sampled_requests_enabled=True
            ),
            rules=[
                wafv2.CfnWebACL.RuleProperty(
                    name="AWSManagedCommon", priority=1,
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS", name="AWSManagedRulesCommonRuleSet"
                        )
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True, metric_name="common", sampled_requests_enabled=True
                    ),
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(none={})
                )
            ]
        )
        wafv2.CfnWebACLAssociation(self, "ApiWafAssoc", resource_arn=api.deployment_stage.stage_arn, web_acl_arn=web_acl.attr_arn)

        # Firehose -> S3
        fh_role = iam.Role(self, "FirehoseRole", assumed_by=iam.ServicePrincipal("firehose.amazonaws.com"))
        processed.grant_read_write(fh_role); data_key.grant_encrypt_decrypt(fh_role)
        delivery = firehose.DeliveryStream(self, "Delivery",
            destinations=[
                destinations.S3Bucket(processed,
                    buffering_interval=Duration.seconds(60),
                    data_output_prefix="year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/",
                    error_output_prefix="errors/!{firehose:error-output-type}/",
                    compression=destinations.Compression.GZIP,
                    logging=True,
                    role=fh_role
                )
            ],
            encryption=firehose.StreamEncryption.KMS, encryption_key=data_key
        )

        # Glue + Crawler
        db = glue.CfnDatabase(self, "Db", catalog_id=self.account, database_input=glue.CfnDatabase.DatabaseInputProperty(name="clickstream"))
        crawler_role = iam.Role(self, "CrawlerRole", assumed_by=iam.ServicePrincipal("glue.amazonaws.com"))
        crawler_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole"))
        processed.grant_read(crawler_role)
        glue.CfnCrawler(self, "Crawler",
            role=crawler_role.role_arn, database_name=db.ref, name="clickstream-processed-crawler",
            targets=glue.CfnCrawler.TargetsProperty(s3_targets=[glue.CfnCrawler.S3TargetProperty(path=f"s3://{processed.bucket_name}/")]),
            schema_change_policy=glue.CfnCrawler.SchemaChangePolicyProperty(delete_behavior="LOG", update_behavior="UPDATE_IN_DATABASE")
        )

        # Athena WorkGroup + results bucket
        results = s3.Bucket(self, "AthenaResults",
            enforce_ssl=True, block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            lifecycle_rules=[s3.LifecycleRule(expiration=Duration.days(90))],
            auto_delete_objects=True, removal_policy=RemovalPolicy.DESTROY
        )
        athena.CfnWorkGroup(self, "WG",
            name="clickstream-wg", state="ENABLED",
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                enforce_work_group_configuration=True,
                result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                    output_location=f"s3://{results.bucket_name}/results/"
                ),
                publish_cloud_watch_metrics_enabled=True
            )
        )

        # Cognito + OpenSearch
        user_pool = cognito.UserPool(self, "UserPool", self_sign_up_enabled=True,
                                     sign_in_aliases=cognito.SignInAliases(email=True))
        user_pool_client = user_pool.add_client("UserPoolClient", auth_flows=cognito.AuthFlow(user_srp=True))
        identity_pool = cognito.CfnIdentityPool(self, "IdentityPool",
            allow_unauthenticated_identities=False,
            cognito_identity_providers=[cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                client_id=user_pool_client.user_pool_client_id,
                provider_name=user_pool.user_pool_provider_name
            )]
        )

        os_sg = ec2.SecurityGroup(self, "OpenSearchSG", vpc=vpc, allow_all_outbound=True)
        for subnet in vpc.private_subnets:
            os_sg.add_ingress_rule(ec2.Peer.ipv4(subnet.ipv4_cidr_block), ec2.Port.tcp(443), "Private subnets to OS")

        master_secret = secrets.Secret(self, "OSMasterSecret",
            generate_secret_string=secrets.SecretStringGenerator(
                secret_string_template='{"username":"master-user"}', generate_string_key="password"
            )
        )

        domain = opensearch.Domain(self, "OpenSearch",
            version=opensearch.EngineVersion.OPENSEARCH_2_13,
            vpc=vpc, vpc_subnets=[ec2.SubnetSelection(subnets=vpc.private_subnets)], security_groups=[os_sg],
            capacity=opensearch.CapacityConfig(data_nodes=2, data_node_instance_type="t3.small.search"),
            ebs=opensearch.EbsOptions(volume_size=20),
            node_to_node_encryption=True,
            encryption_at_rest=opensearch.EncryptionAtRestOptions(enabled=True),
            enforce_https=True,
            fine_grained_access_control=opensearch.AdvancedSecurityOptions(
                master_user_name="master-user",
                master_user_password=master_secret.secret_value_from_json("password")
            ),
            cognito_dashboards_auth=opensearch.CognitoOptions(
                identity_pool_id=identity_pool.ref,
                user_pool_id=user_pool.user_pool_id,
                user_pool_client_id=user_pool_client.user_pool_client_id
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Stream Processor (in VPC) — dual write: Firehose + OpenSearch
        sp = _lambda.Function(self, "StreamProcessor",
            runtime=_lambda.Runtime.PYTHON_3_11, handler="index.handler",
            code=_lambda.Code.from_asset("../lambda/stream_processor"),
            memory_size=512, timeout=Duration.seconds(30),
            vpc=vpc, vpc_subnets=ec2.SubnetSelection(subnets=vpc.private_subnets),
            environment={
                "FIREHOSE_NAME": delivery.delivery_stream_name,
                "OS_ENDPOINT": domain.domain_endpoint,
                "OS_INDEX": "clickstream-events",
                "OS_SECRET_ARN": master_secret.secret_arn,
            }
        )
        stream.grant_read(sp); delivery.grant_put_records(sp)
        master_secret.grant_read(sp)
        sp.add_event_source_mapping("KinesisSource",
            event_source_arn=stream.stream_arn, batch_size=100, starting_position=_lambda.StartingPosition.LATEST,
            bisect_batch_on_error=True
        )

        # Outputs
        cdk.CfnOutput(self, "ApiUrl", value=api.url_for_path("/events"))
        cdk.CfnOutput(self, "KinesisStreamName", value=stream.stream_name)
        cdk.CfnOutput(self, "ProcessedBucketName", value=processed.bucket_name)
        cdk.CfnOutput(self, "OpenSearchEndpoint", value=domain.domain_endpoint)
        cdk.CfnOutput(self, "CognitoUserPoolId", value=user_pool.user_pool_id)
        cdk.CfnOutput(self, "CognitoIdentityPoolId", value=identity_pool.ref)
