# Architecture Review
## Strengths
Managed MQTT, per-device identity, replayable streaming, durable S3 history, separate real-time/search path, explicit anomaly logic, DR and cost governance.

## Tradeoffs
Certificate lifecycle adds fleet-management overhead. OpenSearch adds fixed cost. Dual paths add operational complexity. Exactly-once delivery is not claimed.

## Residual Risks
Reconnect storms, expired certificates, bad firmware floods, clock drift, sequence errors, OpenSearch mapping growth.

## Mitigations
Burst tests, certificate inventory, schema/range checks, last-seen monitoring, controlled mappings, replay procedures.
