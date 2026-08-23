# Acceptance Test Plan

| Test | Method | Pass Condition |
|---|---|---|
| Terraform format | `terraform fmt -check -recursive` | exit 0 |
| Terraform validate | `terraform validate` | exit 0 |
| IaC scan | Trivy config scan | no HIGH/CRITICAL unresolved findings |
| public DB check | config review | RDS `publicly_accessible=false` |
| Multi-AZ DB | config review | `multi_az=true` |
| encryption | config review | RDS/S3/KMS enabled |
| public bucket block | config review | all four public block flags true |
| two-AZ app | config review | two app subnets and desired tasks ≥2 |
| security-group path | config review | DB ingress only from app SG |
| alarms | config review | ALB and RDS alarm resources defined |
| DR documents | document review | RTO/RPO and procedure present |
| FinOps | file review | baseline and savings model reconcile |
| runbook | tabletop | SEV-1, DB, security, backup, cost procedures actionable |
