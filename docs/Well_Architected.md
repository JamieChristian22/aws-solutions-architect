# Well-Architected Highlights

## Operational Excellence
- IaC with CDK; param/store configs; runbooks & canaries; versioned deployments and alarms on SLOs.

## Security
- WAF on API; KMS for S3/DDB; least-privilege IAM; CloudTrail + Security Hub; Secrets Manager; S3 Block Public Access.

## Reliability
- Partitioned lake; retry/backoff; DLQs; multi-AZ services; DR patterns (S3 CRR, Route 53 failover).

## Performance Efficiency
- Event-driven pipelines; DynamoDB for low latency; DAX optional; Redshift Serverless auto-scale; Athena CTAS & partition pruning.

## Cost Optimization
- Serverless-first; lifecycle to Intelligent-Tiering; budgets + anomaly detection; right-sized shards and warehouses.

## Sustainability
- Serverless minimizes idle waste; use managed services; cache to reduce compute.
