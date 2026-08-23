# IAM Least-Privilege Design

## Ingest Lambda
Allowed:
- `kinesis:PutRecord` only on the clickstream stream.
- CloudWatch Logs delivery.

## Processor Lambda
Allowed:
- Kinesis consume permissions via event-source integration.
- `firehose:PutRecord*` only on the delivery stream.
- OpenSearch HTTP write actions only on the selected domain/index.
- KMS use only for required keys.
- CloudWatch Logs.

## Firehose
Allowed:
- write to the processed/error S3 prefixes.
- use the designated KMS key.

No role receives blanket administrator permissions.
