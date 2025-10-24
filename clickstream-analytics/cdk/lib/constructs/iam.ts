import { Construct } from "constructs";
import { aws_iam as iam, aws_s3 as s3, aws_kms as kms } from "aws-cdk-lib";

export class ClickstreamIam extends Construct {
  constructor(scope: Construct, id: string, processedBucket: s3.Bucket, dataKey: kms.Key, firehoseRole: iam.Role) {
    super(scope, id);
    processedBucket.grantReadWrite(firehoseRole);
    dataKey.grantEncryptDecrypt(firehoseRole);
    firehoseRole.addToPolicy(new iam.PolicyStatement({
      actions: ["s3:AbortMultipartUpload","s3:GetBucketLocation","s3:GetObject","s3:ListBucket","s3:ListBucketMultipartUploads","s3:PutObject"],
      resources: [processedBucket.bucketArn, `${processedBucket.bucketArn}/*`]
    }));
  }
}
