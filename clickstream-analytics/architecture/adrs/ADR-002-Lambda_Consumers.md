# ADR-002 — Lambda Stream Consumers
**Status:** Accepted

Lambda is selected because processing is event-driven and stateless. Partial-batch failure handling limits retries to failed records. Long-running ECS consumers may be preferable if processing becomes CPU-heavy or requires sustained connection state.
