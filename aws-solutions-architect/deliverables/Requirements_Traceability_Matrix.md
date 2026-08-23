# Requirements Traceability Matrix

| ID | Requirement | Architecture Control | Validation |
|---|---|---|---|
| NFR-01 | 99.9% availability | ALB + Fargate across 2 AZs; RDS Multi-AZ | AZ-failure game day |
| NFR-02 | RTO ≤ 60 min | warm-standby DR procedure | quarterly DR exercise |
| NFR-03 | RPO ≤ 15 min | automated DB backups/PITR + cross-region copies | restore-point review |
| SEC-01 | private database | DB subnets + SG only from app SG | Terraform/security scan |
| SEC-02 | least privilege | task roles; scoped CI role | IAM policy review |
| SEC-03 | encryption | KMS/SSE + TLS | config validation |
| SEC-04 | audit logging | CloudTrail + Config + log bucket | log delivery test |
| OPS-01 | actionable monitoring | CloudWatch alarms + SNS | alarm test |
| OPS-02 | repeatable deployment | Terraform remote state + CI | plan/apply test |
| FIN-01 | cost allocation | mandatory tags | tag policy check |
| FIN-02 | budget control | budgets/anomaly review process | monthly FinOps review |
