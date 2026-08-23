# Alarm Catalog

| Signal | Threshold | Severity | Response |
|---|---|---|---|
| API 5xx | >1% for 5 min | SEV-2 | check ingest Lambda/APIGW |
| API p95 latency | >250 ms for 10 min | SEV-3 | inspect Lambda/Kinesis latency |
| Ingest Lambda errors | >1% for 5 min | SEV-2 | inspect validation/service errors |
| Ingest throttles | any sustained 5 min | SEV-2 | concurrency/quota review |
| Kinesis iterator age | >60 sec for 3 min | SEV-2 | scale consumer/investigate downstream |
| Kinesis write throttles | >0 for 3 min | SEV-2 | capacity mode/quota |
| Processor Lambda errors | >5 in 10 min | SEV-2 | logs + DLQ |
| Firehose delivery failure | any >5 min | SEV-2 | destination/IAM/KMS |
| DLQ depth | >0 for 10 min | SEV-2 | replay workflow |
| OpenSearch red | any | SEV-1 | cluster recovery |
| OpenSearch yellow | >15 min | SEV-2 | shard/node check |
| OpenSearch JVM pressure | >75% 10 min | SEV-2 | capacity/query review |
| S3 no deliveries | expected volume absent 15 min | SEV-2 | Firehose pipeline |
