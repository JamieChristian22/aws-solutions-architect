# Cost and Security Notes

## Cost Optimization
- Serverless ingestion (Lambda + Kinesis) = no idle EC2 cost.
- S3 is the system of record; Redshift Serverless only holds hot analytics data.
- Partitioned Parquet in S3 reduces Athena scan cost.
- Cold data can age into Glacier for long-term retention.

## Security / Governance
- IAM roles are least-privilege (ingestion Lambda can't read analytics data).
- All data encrypted at rest with KMS and in transit with TLS.
- Lake Formation enforces data-level access by region / role.
- CloudTrail + CloudWatch retained for audit and incident investigation.
