# Operations Runbook
Missing store batch → isolate affected store/date, keep prior curated partition, request resend.
Streaming lag → inspect Kinesis/Lambda, scale consumer, preserve raw landing.
Metric mismatch → stop executive refresh, reconcile fact counts and formulas.
Redshift issue → Athena remains fallback for critical analysis where practical.
