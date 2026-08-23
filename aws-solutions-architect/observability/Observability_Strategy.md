# Observability Strategy

## Golden Signals
**Latency:** ALB target response time and application latency.  
**Traffic:** request count and task throughput.  
**Errors:** HTTP 5xx, application exceptions, failed DB connections.  
**Saturation:** ECS CPU/memory, RDS CPU/connections/storage.

## Logs
- application structured JSON logs to CloudWatch Logs
- ALB/WAF access logs retained for troubleshooting/security
- CloudTrail for control-plane audit
- VPC Flow Logs for network investigation

## SLO
Customer-facing API availability target: **99.9% monthly**.

99.9% monthly availability corresponds to roughly 43 minutes of error-budget downtime in a 30-day month.

## Alarm Philosophy
Alarm on customer impact or imminent capacity failure, not every metric fluctuation. Every SEV-1/SEV-2 alarm has an owner and runbook action.
