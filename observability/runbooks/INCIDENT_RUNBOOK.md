# Incident Runbook (Sample)
1) Alarm triggers (API 5xx or Lambda Errors) → Check CloudWatch Logs (IngestFn).
2) If throttles: raise reserved concurrency or shard count for Kinesis.
3) If malformed events: rollback latest deployment; replay DLQ if configured.
4) If S3 permissions: validate bucket policy and KMS grants.
5) Post-incident: root cause write-up, add regression tests, update alarms.
