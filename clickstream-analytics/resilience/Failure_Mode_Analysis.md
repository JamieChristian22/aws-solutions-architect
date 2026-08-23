# Failure Mode Analysis

| Failure | Effect | Protection | Recovery |
|---|---|---|---|
| ingest Lambda error | event rejected/unaccepted | APIGW error signal | fix/rollback |
| Kinesis backlog | delayed processing | retention + iterator-age alarm | scale consumer |
| processor poison event | retry loop | partial batch failure + DLQ | isolate/replay |
| Firehose outage | lake delay | retries/error output | replay |
| OpenSearch unavailable | search freshness loss | S3 remains authoritative | rebuild/replay |
| Glue/Athena outage | historical query unavailable | S3 data unaffected | service recovery |
| AZ failure | managed services redistribute | multi-AZ service design | automatic/service recovery |
| region outage | ingestion/search unavailable | IaC + cross-region data recovery | DR runbook |
