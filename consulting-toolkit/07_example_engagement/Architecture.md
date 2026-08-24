# Northstar Target Architecture
Route 53 → CloudFront/WAF → ALB → ECS/Fargate private subnets → RDS PostgreSQL Multi-AZ. S3 stores objects/logs. KMS encrypts data. CloudTrail/Config/GuardDuty/Security Hub provide audit/detection. CloudWatch/SNS provide operational alerts. Terraform + GitHub Actions governs changes.
