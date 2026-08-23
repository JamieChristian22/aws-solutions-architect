# Operations Runbook

## Severity Model
| Severity | Example | Ack Target | Owner |
|---|---|---:|---|
| SEV-1 | customer-facing outage / data-access incident | 15 min | incident commander |
| SEV-2 | degraded service / high error rate | 30 min | platform on-call |
| SEV-3 | capacity warning / nonurgent security finding | 4 hr | service owner |

## Application Unavailable
1. Confirm Route 53/CloudFront reachability.
2. Check ALB healthy target count.
3. Check ECS desired vs running tasks and recent deployment events.
4. Review application error logs and task exits.
5. If a bad deployment correlates with incident start, roll back to the prior task definition.
6. Escalate to database checks if application tasks are healthy but requests fail.
7. Record timestamps, actions, and customer impact.

## RDS Performance Incident
1. Check CPU, free memory, DB connections, storage, and latency.
2. Inspect Performance Insights for top waits/queries.
3. Confirm application connection-pool behavior.
4. If capacity is exhausted, apply the approved scaling action.
5. Do not disable Multi-AZ or backup controls to resolve performance.

## Security Finding
1. Triage finding severity and affected principal/resource.
2. Preserve CloudTrail and relevant logs.
3. Disable/limit compromised credentials or role session path.
4. Contain the resource if ongoing exploitation is suspected.
5. Rotate affected secrets.
6. Document root cause and remediation.

## Backup Restore
Follow `resilience/Disaster_Recovery_Plan.md`. Restore to an isolated validation target first, run integrity checks, then approve cutover.

## Cost Spike
1. Review Cost Explorer/anomaly notification.
2. Identify service, account, tag, region, and usage type.
3. Confirm whether spend matches an approved load event.
4. Stop unintended nonproduction resources only after owner validation.
5. Add a preventive control to the FinOps backlog.

## Monthly Operations
- patch/runtime review
- IAM access review
- backup success and restore evidence review
- cost variance review
- critical alarm test
- unused-resource review
