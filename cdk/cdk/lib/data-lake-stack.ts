import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as kinesis from 'aws-cdk-lib/aws-kinesis';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as firehose from 'aws-cdk-lib/aws-kinesisfirehose';

export class DataLakeStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const lake = new s3.Bucket(this, 'Lake', {
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      enforceSSL: true,
      versioned: true
    });

    const stream = new kinesis.Stream(this, 'Events', { shardCount: 1 });

    const role = new iam.Role(this, 'FirehoseRole', {
      assumedBy: new iam.ServicePrincipal('firehose.amazonaws.com')
    });

    lake.grantWrite(role);
    stream.grantRead(role);

    new firehose.CfnDeliveryStream(this, 'ToS3', {
      deliveryStreamType: 'KinesisStreamAsSource',
      kinesisStreamSourceConfiguration: {
        kinesisStreamArn: stream.streamArn,
        roleArn: role.roleArn
      },
      s3DestinationConfiguration: {
        bucketArn: lake.bucketArn,
        roleArn: role.roleArn,
        prefix: 'raw/ingest/year=!{timestamp:YYYY}/month=!{timestamp:MM}/day=!{timestamp:dd}/',
        bufferingHints: { intervalInSeconds: 60, sizeInMBs: 64 },
        compressionFormat: 'GZIP'
      }
    });

    new cdk.CfnOutput(this, 'LakeBucketName', { value: lake.bucketName });
    new cdk.CfnOutput(this, 'KinesisStreamName', { value: stream.streamName });
  }
}
