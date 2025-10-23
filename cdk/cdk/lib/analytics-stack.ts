import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as glue from 'aws-cdk-lib/aws-glue';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class AnalyticsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Reference existing lake bucket by export or parameter, simplified here
    const lakeName = new cdk.CfnParameter(this, 'LakeBucketName', { type: 'String' }).valueAsString;
    const lake = s3.Bucket.fromBucketName(this, 'Lake', lakeName);

    const db = new glue.CfnDatabase(this, 'Db', {
      catalogId: cdk.Aws.ACCOUNT_ID,
      databaseInput: { name: 'retail_analytics' }
    });

    new glue.CfnCrawler(this, 'RawCrawler', {
      role: 'AWSGlueServiceRoleDefault', // replace with a managed role in real env
      databaseName: db.ref,
      targets: { s3Targets: [{ path: f's3://{lake.bucketName}/raw/ingest/' }] },
      name: 'retail-raw-crawler'
    });
  }
}
