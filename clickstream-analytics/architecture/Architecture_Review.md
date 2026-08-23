# Architecture Review

## Strengths
- fully managed ingestion and stream services
- independent near-real-time and historical analytics paths
- durable S3 system of record
- replayable stream/error design
- schema governance
- VPC/private search tier
- explicit capacity, cost, and recovery models

## Tradeoffs
- dual-write increases processor complexity
- OpenSearch can become a major fixed-cost component
- serverless components simplify operations but require careful concurrency/throttle management
- exactly-once semantics are not claimed; consumers are idempotent by event ID

## Residual Risks
- unusually large traffic spikes can increase iterator age
- malformed client instrumentation can generate high-volume low-value events
- OpenSearch schema explosions are possible if arbitrary property keys are indexed
- a large number of tiny S3 objects can reduce query efficiency

## Mitigations
- event allowlist and payload limits
- event ID deduplication strategy
- strict OpenSearch mappings
- Firehose buffering/compaction
- anomaly alerts and traffic quotas
