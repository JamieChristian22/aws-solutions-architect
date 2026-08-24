# Security Assessment

| Domain | Finding | Severity | Recommendation |
|---|---|---:|---|
| IAM | broad human admin | High | federation + role separation |
| Secrets | app secrets in environment files | High | Secrets Manager |
| Network | database reachable from broad CIDR | High | SG-to-SG only |
| Logging | CloudTrail not centralized | Medium | centralized audit bucket |
| Detection | GuardDuty absent | Medium | enable GuardDuty/Security Hub |
| S3 | mixed public-access posture | High | account/bucket public block |
| Encryption | default keys only | Medium | customer-managed KMS where required |
| DR | restore not tested | High | quarterly recovery exercises |
