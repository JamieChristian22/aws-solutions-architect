# Data Quality Rules

1. `event_id`, `event_time`, `session_id`, `anonymous_id`, `event_type`, and `page_url` are required.
2. `event_id` must be unique within the configured deduplication horizon.
3. `event_time` cannot be more than 5 minutes in the future.
4. event types must be from the schema allowlist.
5. purchase revenue must be nonnegative.
6. payload must remain below 64 KB.
7. arbitrary top-level fields are rejected.
8. property maps are limited to 20 keys.
9. malformed records are routed to the error path with the rejection reason.
10. user/session identifiers are treated as pseudonymous identifiers and should not contain direct PII.
