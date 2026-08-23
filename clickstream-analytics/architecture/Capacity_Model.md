# Capacity and Throughput Model

## Assumptions
- Sustained rate: **1,000 events/sec**
- Peak rate: **5,000 events/sec**
- Average serialized event: **1,024 bytes**
- Sustained operation: 24 hours/day
- Parquet compression/columnar footprint assumption: **22% of raw**

## Calculations

`events/day = events/sec × 86,400`

`raw bytes/day = events/day × average event bytes`

| Metric | Result |
|---|---:|
| Sustained events/day | 86,400,000 |
| Raw GB/day | 88.47 |
| Raw TB/30 days | 2.65 |
| Parquet TB/30 days | 0.58 |
| Peak/raw MB/sec | 5.12 MB/sec |

## Kinesis
On-demand mode is selected in the reference CDK because traffic is expected to be bursty. Provisioned mode can be cheaper for predictable traffic, but must be sized and monitored for write/read limits.

## Lambda Consumer
Batch size is bounded so one poison record does not create an oversized replay set. Partial batch response is enabled so successfully processed Kinesis records are not retried unnecessarily.

## Firehose
Buffering is optimized for analytics freshness rather than per-record immediacy. The design target is <15 minutes to S3, with Parquet conversion and date/hour/event-type partitioning.

## OpenSearch
OpenSearch is sized by indexing rate, retention period, query concurrency, shard count, and storage. The serving tier is intentionally not treated as the durable record store.

## Load Test Gates
Before production:
1. sustain 1,000 events/sec for 30 minutes;
2. burst to 5,000 events/sec for 10 minutes;
3. verify no uncontrolled iterator-age growth;
4. verify error/DLQ rate <0.1%;
5. verify OpenSearch freshness <60 sec p95;
6. verify S3 freshness <15 min p95.
