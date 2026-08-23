# Customer Discovery Workshop

## Business Goals
- Support 3× user growth without redesigning the platform.
- Improve availability from a single-AZ dependency to a 99.9% target.
- Establish repeatable infrastructure deployment.
- Reduce security audit gaps.
- Create cost ownership and monthly variance review.
- Establish regional disaster recovery.

## Current-State Findings
| Area | Current State | Risk |
|---|---|---|
| Compute | manually managed instances | patching and inconsistent scaling |
| Database | single-AZ relational database | availability risk |
| Networking | mixed public/private placement | excess exposure |
| Logging | service-by-service | weak auditability |
| Deployments | manual console changes | drift/change risk |
| Cost | no enforced tagging | poor allocation |
| Recovery | backups exist but no tested restore | uncertain RTO |

## Nonfunctional Requirements
- 99.9% availability target.
- 60-minute regional RTO.
- 15-minute transactional RPO target.
- Encryption at rest and in transit.
- No public database endpoints.
- No permanent AWS access keys for workloads.
- Infrastructure changes reviewed through pull requests.
- Critical security findings triaged within four hours.
- High-severity operational alerts acknowledged within 15 minutes.

## Constraints
- Primary region remains `us-east-1`.
- Team has Terraform familiarity but no Kubernetes operating model.
- First delivery window is 90 days.
- Architecture should minimize undifferentiated operations.

## Stakeholders
| Role | Responsibility |
|---|---|
| CTO | executive sponsor |
| Engineering Lead | application owner |
| Security Lead | control approval |
| Finance Partner | cost governance |
| Platform Engineer | Terraform/operations |
| Solutions Architect | design and delivery leadership |
