import { Construct } from "constructs";
import { Stack, Duration, RemovalPolicy } from "aws-cdk-lib";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as athena from "aws-cdk-lib/aws-athena";
import * as glue from "aws-cdk-lib/aws-glue";

export class ClickstreamAthena extends Construct {
  public readonly resultsBucket: s3.Bucket;
  public readonly workgroup: athena.CfnWorkGroup;
  public readonly database: glue.CfnDatabase;
  public readonly table: glue.CfnTable;

  constructor(scope: Construct, id: string, processedBucket: s3.Bucket) {
    super(scope, id);
    this.resultsBucket = new s3.Bucket(this, "AthenaResults", {
      enforceSSL: true, blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      lifecycleRules: [{ expiration: Duration.days(90) }],
      removalPolicy: RemovalPolicy.DESTROY, autoDeleteObjects: true
    });
    this.workgroup = new athena.CfnWorkGroup(this, "WG", {
      name: "clickstream-wg", state: "ENABLED",
      workGroupConfiguration: { enforceWorkGroupConfiguration: true, resultConfiguration: { outputLocation: `s3://${this.resultsBucket.bucketName}/results/` }, publishCloudWatchMetricsEnabled: True }
    } as any);
    this.database = new glue.CfnDatabase(this, "Db", { catalogId: Stack.of(this).account, databaseInput: { name: "clickstream" } });
    this.table = new glue.CfnTable(this, "Events", {
      catalogId: Stack.of(this).account, databaseName: this.database.ref,
      tableInput: {
        name: "events", tableType: "EXTERNAL_TABLE",
        parameters: { "classification": "parquet", "parquet.compression": "GZIP", "EXTERNAL": "TRUE" },
        storageDescriptor: {
          location: `s3://${processedBucket.bucketName}/`, compressed: true,
          inputFormat: "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
          outputFormat: "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
          serdeInfo: { serializationLibrary: "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe", parameters: { "serialization.format": "1" } },
          columns: [
            { name: "event_name", type: "string" }, { name: "user_id", type: "string" }, { name: "created_at", type: "string" },
            { name: "received_at", type: "string" }, { name: "user_agent", type: "string" }, { name: "origin", type: "string" },
            { name: "element_clicked", type: "string" }, { name: "time_spent", type: "int" }, { name: "source_menu", type: "string" }, { name: "page_url", type: "string" }
          ]
        },
        partitionKeys: [ { name: "year", type: "string" }, { name: "month", type: "string" }, { name: "day", type: "string" }, { name: "hour", type: "string" } ]
      }
    });
  }
}
