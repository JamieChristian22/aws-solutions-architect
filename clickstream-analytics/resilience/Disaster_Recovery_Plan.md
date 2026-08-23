# Disaster Recovery Plan

## Targets
- RTO: 60 minutes
- RPO: ≤5 minutes for records successfully accepted into the stream/lake path

## Regional Strategy
Primary: `us-east-1`  
Recovery: `us-west-2`

Critical durable data is S3-based and should use cross-region replication for production-class deployment. CDK recreates API, Kinesis, Lambdas, Firehose, Glue, OpenSearch, WAF, IAM, and alarms in the recovery region.

## Recovery Procedure
1. Declare regional incident.
2. Confirm last replicated S3 object and accepted-event window.
3. Deploy CDK stack to recovery region.
4. Validate KMS/IAM and S3 replication destination.
5. Restore/rebuild OpenSearch indexes from durable data.
6. Run smoke tests.
7. Switch client endpoint/DNS/config to recovery API.
8. Monitor accepted events, iterator age, Firehose delivery, and search freshness.
9. Record actual RTO/RPO achieved.

## Quarterly Exercise
Run a tabletop every quarter and a technical recovery test at least twice per year.
