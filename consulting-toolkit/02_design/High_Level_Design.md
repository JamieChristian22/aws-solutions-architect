# High-Level Design

## Reference Pattern
Route 53 → CloudFront/WAF → ALB/API Gateway → private compute → managed data services.

## Cross-Cutting Controls
- federation and role-based access
- KMS encryption
- CloudTrail / Config / GuardDuty / Security Hub
- CloudWatch alarms and logs
- Terraform/CDK IaC
- backups + tested recovery
- tags + budget ownership

## NFRs
Availability: 99.9%  
RTO: 60 minutes  
RPO: 15 minutes  
Critical-alert acknowledgement: 15 minutes  
Infrastructure drift: zero unmanaged production changes
