# Threat Model
- stolen cert → per-device revocation
- topic abuse → client/topic-scoped policy
- replay/duplicates → sequence/event-time validation
- malformed firmware → schema/range checks
- reconnect storm → managed IoT Core + Kinesis buffer
- data exposure → private search, S3 block, IAM/KMS
- silent device → last-seen alarms
