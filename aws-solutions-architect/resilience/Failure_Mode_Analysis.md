# Failure Mode Analysis

| Failure | Expected Behavior | Detection | Recovery |
|---|---|---|---|
| one ECS task fails | service replaces task | running task count/alarm | automatic replacement |
| one AZ unavailable | ALB routes to healthy AZ | target health/AZ metrics | scale surviving AZ; AWS service recovery |
| RDS primary failure | Multi-AZ failover | RDS event/connection errors | reconnect after managed failover |
| bad application release | elevated errors | 5xx/error alarms | rollback task definition |
| NAT gateway failure | outbound calls affected in one AZ | app errors/route diagnostics | use per-AZ NAT path / replace |
| S3 object deletion | versioned object recoverable | audit/application error | restore prior version |
| region outage | primary unavailable | multi-signal incident | execute DR plan |
| CI credential abuse | suspicious role session | CloudTrail/GuardDuty | revoke trust/session path and investigate |
