# Data Flow
1. Device publishes to `axis/{site_id}/{device_id}/telemetry` over MQTT/TLS.
2. IoT Core authenticates its unique X.509 certificate and policy.
3. IoT Rule sends telemetry to Kinesis.
4. Lambda validates/enriches telemetry and detects anomalies.
5. Anomalies publish to SNS.
6. Recent telemetry is available to OpenSearch.
7. Curated data enters Firehose/S3 for durable history.
8. Glue/Athena/QuickSight provide historical analytics.
