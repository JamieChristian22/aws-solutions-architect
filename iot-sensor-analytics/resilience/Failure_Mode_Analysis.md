# Failure Modes
Device offline → last-seen alert. Cert expiry → rotate. Reconnect storm → Kinesis buffer. Poison message → isolate/replay. Kinesis backlog → scale consumer. OpenSearch outage → S3 remains authoritative. Firehose failure → retry/error path. Region outage → execute DR.
