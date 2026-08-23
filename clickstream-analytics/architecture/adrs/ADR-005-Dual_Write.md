# ADR-005 — Dual Write with Durable Lake Priority
**Status:** Accepted

The processor attempts both Firehose/S3 and OpenSearch delivery. If OpenSearch indexing fails, the record is retained for replay and the S3 path remains authoritative. The design prioritizes durable historical capture over search freshness.
