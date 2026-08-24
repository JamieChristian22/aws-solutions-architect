# Security Control Evidence Map

| Control Objective | Architecture Evidence | Validation Evidence |
|---|---|---|
| restrict PHI access | Lake Formation + IAM design | access-policy review |
| encrypt at rest | KMS-backed S3 | CDK static review |
| prevent public storage | S3 public access block | CDK static review |
| maintain auditability | CloudTrail/audit zone design | logging checklist |
| protect analytics users from raw PHI | curated de-identified zone | de-identification rules |
| recover data | versioning / DR strategy | DR plan and restore checklist |

This is a technical-control evidence map, not a legal compliance attestation.
