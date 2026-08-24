# HIPAA-Aligned Technical Control Matrix

| Safeguard Area | Technical Pattern | Evidence |
|---|---|---|
| access control | federated roles, least privilege | IAM policy review |
| audit controls | CloudTrail/Lake access logs | centralized log bucket |
| integrity | versioning/checksums/validation | data-quality reports |
| transmission security | TLS/private endpoints | config review |
| contingency | backups/DR | restore exercise |
| minimum necessary | role/table/column grants | Lake Formation grants |

Compliance requires organizational/legal/process controls beyond this architecture.
