# Threat Model

| Threat | Example | Controls |
|---|---|---|
| event flooding | bot sends huge volume | WAF rate rules, APIGW throttles, budgets |
| malformed payloads | schema abuse | JSON schema, payload size limit |
| injection/mapping explosion | arbitrary properties | strict schema, OpenSearch mappings |
| credential misuse | leaked CI/user keys | roles, federation/OIDC, no static workload keys |
| data exposure | public S3/search endpoint | block public access, VPC search, IAM |
| event tampering | unauthorized publisher | API auth pattern, TLS, audit logs |
| destructive control-plane action | resource deletion | CloudTrail, scoped IAM, retained buckets |
| PII leakage | direct personal data in events | instrumentation contract prohibits direct PII |
