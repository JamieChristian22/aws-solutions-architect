# Threat Model

## Assets
- customer application data
- database credentials and secrets
- AWS control-plane permissions
- audit logs
- application container images
- Terraform state

## Threats and Controls
| Threat | Attack Path | Primary Controls | Detection |
|---|---|---|---|
| credential theft | developer/CI credentials | federation, MFA, OIDC, short-lived roles | CloudTrail, GuardDuty |
| data exfiltration | public bucket / broad IAM | public-access block, bucket policies, least privilege | Config, Security Hub |
| SQL/application compromise | malicious requests | WAF, app auth, private DB, patching | WAF logs, app logs |
| privilege escalation | overbroad IAM | scoped roles, reviews, permission boundaries where needed | IAM review, CloudTrail |
| ransomware/destructive action | delete/overwrite resources | backups, versioning, deletion protection, restricted admin | CloudTrail, backup monitoring |
| supply-chain compromise | dependency or IaC change | PR review, pinned actions, IaC scanning | CI results |
| DDoS/traffic abuse | Internet edge | CloudFront, WAF rate rules, AWS Shield Standard | CloudWatch/WAF metrics |

## Trust Boundaries
Internet → edge → ALB → application tasks → database/secrets is treated as a sequence of separate trust boundaries. No single network location grants data access by itself.
