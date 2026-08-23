# Security Posture Checklist

## Identity
- [x] Human access designed for federation and MFA.
- [x] Workloads use IAM roles.
- [x] GitHub Actions uses OIDC federation.
- [x] Administrative permissions separated from application roles.
- [x] IAM policies avoid wildcard actions unless explicitly justified.

## Network
- [x] Database tier has no public subnet placement.
- [x] Application tasks run in private subnets.
- [x] Security groups use least-required inbound paths.
- [x] Public ingress terminates at edge/ALB.
- [x] VPC flow logs included in observability design.

## Data
- [x] S3 public access blocked.
- [x] RDS encryption enabled.
- [x] Secrets Manager used for secrets.
- [x] TLS expected for application/database connections.
- [x] Backups have retention and restore-test procedures.

## Detection
- [x] CloudTrail enabled.
- [x] AWS Config enabled.
- [x] GuardDuty enabled.
- [x] Security Hub enabled.
- [x] Critical findings route to an incident channel.

## Application Edge
- [x] WAF managed rule groups.
- [x] Rate-based rule.
- [x] TLS certificate management.
- [x] Access logging.
