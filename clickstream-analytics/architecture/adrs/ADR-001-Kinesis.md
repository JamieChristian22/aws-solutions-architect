# ADR-001 — Kinesis Data Streams
**Status:** Accepted

Kinesis is used for ordered, replayable real-time event ingestion. SQS is excellent for work queues but does not provide the same stream/replay semantics for analytics consumers. MSK is more operationally complex than required for this portfolio scenario.
