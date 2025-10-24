import { Construct } from "constructs";
import { Stack } from "aws-cdk-lib";
import { aws_glue as glue, aws_iam as iam, aws_s3 as s3 } from "aws-cdk-lib";

export class ClickstreamGlue extends Construct {
  public readonly database: glue.CfnDatabase;
  public readonly crawler: glue.CfnCrawler;
  constructor(scope: Construct, id: string, processedBucket: s3.Bucket) {
    super(scope, id);
    this.database = new glue.CfnDatabase(this, "Db", { catalogId: Stack.of(this).account, databaseInput: { name: "clickstream" } });
    const role = new iam.Role(this, "CrawlerRole", { assumedBy: new iam.ServicePrincipal("glue.amazonaws.com") });
    processedBucket.grantRead(role);
    role.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName("service-role/AWSGlueServiceRole"));
    this.crawler = new glue.CfnCrawler(this, "Crawler", {
      role: role.roleArn, databaseName: this.database.ref, name: "clickstream-processed-crawler",
      targets: { s3Targets: [{ path: `s3://${processedBucket.bucketName}/` }] },
      schemaChangePolicy: { deleteBehavior: "LOG", updateBehavior: "UPDATE_IN_DATABASE" }
    });
  }
}
