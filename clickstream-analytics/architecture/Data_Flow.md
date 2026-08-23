# End-to-End Data Flow

## 1. Client
Clients generate JSON clickstream events with event ID, timestamp, anonymous/user ID, session ID, event type, page/feature context, source, campaign, device, and properties.

## 2. Ingestion
API Gateway provides the managed HTTP surface. WAF applies AWS managed rules and a rate-based rule. Ingest Lambda validates the JSON schema and rejects oversized/invalid payloads.

## 3. Stream
Validated events are placed on Kinesis using `session_id` as the partition key. This preserves within-session ordering while distributing traffic across many sessions.

## 4. Processing
Processor Lambda:
- validates required fields again;
- adds processing metadata;
- sends records to Firehose for the lake;
- indexes records into OpenSearch;
- emits CloudWatch custom metrics;
- isolates failed records for retry/replay.

## 5. Data Lake
Firehose converts JSON to Parquet and writes partitioned S3 objects. Glue provides catalog metadata. Athena queries use date/hour/event_type filters to minimize scanning.

## 6. Search
OpenSearch indexes a subset of fields optimized for low-latency user/session/event exploration.

## 7. Operations
Metrics, logs, and DLQ/error prefixes allow operators to determine whether failures originate in ingestion, stream consumption, delivery, indexing, or downstream query services.
