# Solution Design Document

## 1. Business Context
Northstar Digital Services needs a secure and repeatable AWS platform for a B2B SaaS application. The design prioritizes reliability, least privilege, operational visibility, recoverability, and cost governance.

## 2. Target Architecture
- Route 53 DNS.
- CloudFront at the edge.
- AWS WAF attached to the public entry path.
- Application Load Balancer across two public subnets.
- ECS Fargate service in two private application subnets.
- RDS PostgreSQL Multi-AZ in isolated database subnets.
- S3 for application assets and centralized logs.
- Secrets Manager for database/application secrets.
- KMS-backed encryption.
- CloudWatch metrics/logs and SNS notifications.
- CloudTrail, AWS Config, GuardDuty, and Security Hub.
- AWS Backup / RDS automated backup controls.
- Cross-region recovery assets in `us-west-2`.

## 3. Network
Primary VPC CIDR: `10.40.0.0/16`. Public, application, and database tiers have separate subnets in two Availability Zones. Databases have no route to the Internet Gateway. Security groups reference other security groups instead of broad CIDR rules where possible.

## 4. Identity
Human access uses federated identities with MFA. Workloads use IAM roles. GitHub Actions uses OIDC federation instead of stored AWS access keys. Production apply is tied to an environment approval gate.

## 5. Data Protection
- RDS encrypted at rest and uses TLS.
- S3 buckets block public access and use encryption.
- Secrets are stored in Secrets Manager.
- Audit logs are retained separately from application data.
- Deletion protection is enabled for production database resources.

## 6. Availability
ALB and Fargate run across two AZs. RDS uses Multi-AZ. Application tasks are configured with a minimum healthy capacity of two. Autoscaling responds to CPU and request load.

## 7. Disaster Recovery
Regional failure uses documented warm-standby recovery. Infrastructure is reproducible from Terraform. RDS recovery uses cross-region snapshot copies/backup strategy; S3 uses replication for designated data sets. Route 53 cutover occurs after application and data validation.

## 8. Observability
Four signal categories are monitored:
- availability: target health, synthetic endpoint checks
- latency: ALB target response time and application latency
- errors: HTTP 5xx, application exception rate
- saturation: CPU, memory, DB connections/storage

## 9. Security
WAF limits common web attacks; GuardDuty and Security Hub centralize threat and posture findings. CloudTrail provides API audit history. AWS Config detects drift from required controls.

## 10. Cost
Baseline cost governance relies on tags, budget thresholds, anomaly review, storage lifecycle, autoscaling, and rightsizing. Commitment discounts are evaluated only after the workload has stable measured utilization.

## 11. Risks
| Risk | Impact | Mitigation |
|---|---|---|
| credential misuse | high | federation, MFA, role-based access, OIDC |
| public data exposure | high | bucket public-access block, private DB, policy scans |
| cost spike | medium | budgets, anomaly monitoring, autoscaling limits |
| regional outage | high | DR runbook, cross-region data recovery, quarterly tests |
| deployment defect | high | CI validation, reviewed plan, protected apply |
| observability noise | medium | severity model and actionable alarm thresholds |

## 12. Acceptance Criteria
All items in `validation/Acceptance_Test_Plan.md` must pass or have a documented risk acceptance.
