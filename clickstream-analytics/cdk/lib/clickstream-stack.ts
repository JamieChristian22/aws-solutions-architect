import { Stack, StackProps, Duration, RemovalPolicy, CfnOutput } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as kms from "aws-cdk-lib/aws-kms";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as iam from "aws-cdk-lib/aws-iam";
import * as logs from "aws-cdk-lib/aws-logs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigw from "aws-cdk-lib/aws-apigateway";
import * as wafv2 from "aws-cdk-lib/aws-wafv2";
import * as kds from "aws-cdk-lib/aws-kinesis";
import * as firehose from "aws-cdk-lib/aws-kinesisfirehose";
import * as s3dest from "aws-cdk-lib/aws-kinesisfirehose-destinations";
import * as eventsrc from "aws-cdk-lib/aws-lambda-event-sources";
import { ClickstreamVpc } from "./constructs/vpc";
import { ClickstreamIam } from "./constructs/iam";
import { ClickstreamGlue } from "./constructs/glue";
import { ClickstreamAthena } from "./constructs/athena";
import { ClickstreamOpenSearch } from "./constructs/opensearch";

export class ClickstreamStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const vpc = new ClickstreamVpc(this, "Net").vpc;
    const key = new kms.Key(this, "DataKey", { enableKeyRotation: true, alias: "alias/clickstream-data" });

    const processed = new s3.Bucket(this, "Processed", {
      encryption: s3.BucketEncryption.KMS, encryptionKey: key, blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL, enforceSSL: true,
      lifecycleRules: [{ expiration: Duration.days(365) }], removalPolicy: RemovalPolicy.DESTROY, autoDeleteObjects: true
    });
    const bad = new s3.Bucket(this, "Bad", {
      encryption: s3.BucketEncryption.KMS, encryptionKey: key, blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL, enforceSSL: true,
      lifecycleRules: [{ expiration: Duration.days(30) }], removalPolicy: RemovalPolicy.DESTROY, autoDeleteObjects: true
    });

    const stream = new kds.Stream(this, "EventStream", {
      shardCount: 1, streamMode: kds.StreamMode.PROVISIONED, encryption: kds.StreamEncryption.KMS, encryptionKey: key,
      retentionPeriod: Duration.hours(24)
    });

    const ingest = new lambda.Function(this, "IngestFn", {
      runtime: lambda.Runtime.NODEJS_20_X, handler: "index.handler", code: lambda.Code.fromAsset("../lambda/ingest"),
      memorySize: 256, timeout: Duration.seconds(10),
      environment: { STREAM_NAME: stream.streamName, BAD_BUCKET: bad.bucketName, ALLOW_ORIGINS: "https://localhost,https://example.com" },
      logRetention: logs.RetentionDays.ONE_WEEK
    });
    stream.grantWrite(ingest);
    bad.grantWrite(ingest);

    const api = new apigw.RestApi(this, "Api", { deployOptions: { stageName: "prod", loggingLevel: apigw.MethodLoggingLevel.INFO } });
    api.root.addResource("events").addMethod("POST", new apigw.LambdaIntegration(ingest));

    const webAcl = new wafv2.CfnWebACL(this, "ApiWaf", {
      defaultAction: { allow: {} }, scope: "REGIONAL", name: "clickstream-api-waf",
      visibilityConfig: { cloudWatchMetricsEnabled: true, metricName: "api-waf", sampledRequestsEnabled: true },
      rules: [{ name: "ManagedCommon", priority: 1, statement: { managedRuleGroupStatement: { vendorName: "AWS", name: "AWSManagedRulesCommonRuleSet" } },
        visibilityConfig: { cloudWatchMetricsEnabled: true, metricName: "common", sampledRequestsEnabled: true }, overrideAction: { none: {} } }]
    });
    new wafv2.CfnWebACLAssociation(this, "WafAssoc", { resourceArn: api.deploymentStage.stageArn, webAclArn: webAcl.attrArn });

    const fhRole = new iam.Role(this, "FirehoseRole", { assumedBy: new iam.ServicePrincipal("firehose.amazonaws.com") });
    const delivery = new firehose.DeliveryStream(this, "Delivery", {
      destinations: [ new s3dest.S3Bucket(processed, { bufferingInterval: Duration.seconds(60), dataOutputPrefix: "year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/",
        errorOutputPrefix: "errors/!{firehose:error-output-type}/", compression: s3dest.Compression.GZIP, logging: true, role: fhRole }) ],
      encryption: firehose.StreamEncryption.KMS, encryptionKey: key
    });
    new ClickstreamIam(this, "Iam", processed, key, fhRole);

    // Stream processor Lambda in VPC to forward to Firehose (and optionally OS)
    const sp = new lambda.Function(this, "StreamProcessor", {
      runtime: lambda.Runtime.NODEJS_20_X, handler: "index.handler", code: lambda.Code.fromAsset("../lambda/stream-processor"),
      memorySize: 512, timeout: Duration.seconds(30), vpc, vpcSubnets: { subnets: vpc.privateSubnets },
      environment: { FIREHOSE_NAME: delivery.deliveryStreamName }
    });
    stream.grantRead(sp);
    delivery.grantPutRecords(sp);
    sp.addEventSource(new eventsrc.KinesisEventSource(stream, { batchSize: 100, startingPosition: lambda.StartingPosition.LATEST }));

    // Glue + Athena
    new ClickstreamGlue(this, "Glue", processed);
    new ClickstreamAthena(this, "Athena", processed);

    // OpenSearch (optional; VPC only)
    new ClickstreamOpenSearch(this, "OS", vpc);

    new CfnOutput(this, "ApiUrl", { value: api.urlForPath("/events") });
    new CfnOutput(this, "ProcessedBucket", { value: processed.bucketName });
  }
}
