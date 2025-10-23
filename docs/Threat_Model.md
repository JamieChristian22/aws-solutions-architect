# Threat Model (STRIDE summary)
- **Spoofing**: Cognito / JWT validation, WAF, mTLS (optional), signed requests.
- **Tampering**: KMS encryption, S3 Object Lock (governance), versioning, CloudTrail.
- **Repudiation**: Centralized logs, immutable audit via CloudTrail + CloudWatch.
- **Information Disclosure**: VPC endpoints, least-privilege, Macie, tokenized PII fields.
- **Denial of Service**: WAF managed rules, throttling, Kinesis shard scaling, autoscaling concurrency limits.
- **Elevation of Privilege**: Fine-grained IAM, no wildcards in prod, approvals for pipeline to prod.
