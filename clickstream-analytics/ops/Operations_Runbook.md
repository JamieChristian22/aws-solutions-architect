# Operations Runbook

## SEV-1: Ingestion Unavailable
1. Verify API Gateway health and WAF blocks.
2. Check ingest Lambda error/throttle metrics.
3. Check Kinesis write-throttled records.
4. Confirm IAM/KMS failures in logs.
5. If deployment-correlated, roll back the last CDK/application change.
6. Validate with one known-good sample event.
7. Track event-loss window and communicate impact.

## SEV-2: Iterator Age Growing
1. Check processor errors/throttles.
2. Check OpenSearch and Firehose latency/failures.
3. Increase Lambda reserved concurrency/parallelization only within downstream capacity.
4. If OpenSearch is the bottleneck, temporarily prioritize S3 durability and replay search writes later.
5. Verify iterator age returns toward zero.

## Firehose/S3 Failure
1. Inspect delivery stream errors and destination access.
2. Verify S3 bucket/KMS permissions.
3. Check error output prefix.
4. Correct configuration and replay retained records.

## OpenSearch Failure
1. Inspect cluster status, JVM pressure, storage, rejected requests.
2. Preserve S3 delivery path.
3. Reduce search write pressure if required.
4. Restore/rebuild index from S3/replay path after cluster recovery.

## DLQ Replay
1. Export failed messages/records.
2. Identify root cause.
3. Correct transformation/mapping.
4. Replay in bounded batches.
5. Confirm event IDs prevent unintended duplicates.
6. Archive replay evidence.

## Monthly
- review cost by service
- inspect Athena scan efficiency
- review partition/object size
- review OpenSearch index lifecycle
- test alarms
- sample schema rejection rates
