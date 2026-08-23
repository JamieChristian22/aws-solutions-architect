# ADR-006 — Regional Recovery
**Status:** Accepted

The project uses infrastructure-as-code rebuild plus replicated/backed-up durable data. Active/active multi-region streaming is not selected because the 60-minute RTO does not justify the added cost and operational complexity.
