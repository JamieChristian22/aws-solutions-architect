# ADR-003 — Parquet + Date/Hour/Event-Type Partitioning
**Status:** Accepted

S3 data is stored in Parquet and partitioned by event_date, event_hour, and event_type. High-cardinality fields such as user/session ID are not partitions. This balances Athena pruning with object/partition manageability.
