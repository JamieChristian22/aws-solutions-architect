from aws_cdk import Stack,Duration,RemovalPolicy,CfnOutput,aws_iot as iot,aws_kinesis as kinesis,aws_kms as kms,aws_lambda as _lambda,aws_lambda_event_sources as es,aws_s3 as s3,aws_sns as sns,aws_sqs as sqs,aws_iam as iam,aws_firehose as firehose
from constructs import Construct
class IoTSensorAnalyticsStack(Stack):
    def __init__(self,scope,id,**kwargs):
        super().__init__(scope,id,**kwargs)
        key=kms.Key(self,"Key",enable_key_rotation=True)
        stream=kinesis.Stream(self,"Telemetry",stream_mode=kinesis.StreamMode.ON_DEMAND,encryption=kinesis.StreamEncryption.KMS,encryption_key=key,retention_period=Duration.hours(48))
        lake=s3.Bucket(self,"Lake",encryption=s3.BucketEncryption.KMS,encryption_key=key,block_public_access=s3.BlockPublicAccess.BLOCK_ALL,enforce_ssl=True,versioned=True,removal_policy=RemovalPolicy.RETAIN)
        alerts=sns.Topic(self,"Alerts",master_key=key)
        dlq=sqs.Queue(self,"DLQ",encryption=sqs.QueueEncryption.KMS,encryption_master_key=key,retention_period=Duration.days(14))
        role=iam.Role(self,"FirehoseRole",assumed_by=iam.ServicePrincipal("firehose.amazonaws.com")); lake.grant_read_write(role); key.grant_encrypt_decrypt(role)
        delivery=firehose.CfnDeliveryStream(self,"Delivery",delivery_stream_type="DirectPut",extended_s3_destination_configuration=firehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty(bucket_arn=lake.bucket_arn,role_arn=role.role_arn,prefix="telemetry/event_date=!{timestamp:yyyy-MM-dd}/event_hour=!{timestamp:HH}/",error_output_prefix="errors/!{firehose:error-output-type}/",buffering_hints=firehose.CfnDeliveryStream.BufferingHintsProperty(interval_in_seconds=300,size_in_m_bs=64),compression_format="GZIP"))
        fn=_lambda.Function(self,"Processor",runtime=_lambda.Runtime.PYTHON_3_11,handler="index.handler",code=_lambda.Code.from_asset("../lambda/stream_processor"),memory_size=512,timeout=Duration.seconds(30),environment={"ALERT_TOPIC_ARN":alerts.topic_arn,"DELIVERY_STREAM":delivery.ref},dead_letter_queue=dlq)
        alerts.grant_publish(fn)
        fn.add_to_role_policy(iam.PolicyStatement(actions=["firehose:PutRecord","firehose:PutRecordBatch"],resources=[delivery.attr_arn]))
        fn.add_event_source(es.KinesisEventSource(stream,starting_position=_lambda.StartingPosition.LATEST,batch_size=200,retry_attempts=5,bisect_batch_on_error=True,report_batch_item_failures=True))
        rule_role=iam.Role(self,"IoTRuleRole",assumed_by=iam.ServicePrincipal("iot.amazonaws.com")); stream.grant_write(rule_role)
        iot.CfnTopicRule(self,"TelemetryRule",topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(sql="SELECT * FROM 'axis/+/+/telemetry'",aws_iot_sql_version="2016-03-23",actions=[iot.CfnTopicRule.ActionProperty(kinesis=iot.CfnTopicRule.KinesisActionProperty(role_arn=rule_role.role_arn,stream_name=stream.stream_name,partition_key="${device_id}"))]))
        CfnOutput(self,"StreamName",value=stream.stream_name); CfnOutput(self,"LakeBucket",value=lake.bucket_name); CfnOutput(self,"AlertTopic",value=alerts.topic_arn)
