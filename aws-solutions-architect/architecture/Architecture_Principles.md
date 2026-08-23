# Architecture Principles

## Reliability
Production workloads span at least two Availability Zones. Stateless compute is replaceable. Stateful recovery is based on managed backups, point-in-time recovery, and documented restore tests.

## Security
Identity is role-based; public exposure is limited to the edge and load balancer. KMS encryption, TLS, centralized audit logs, AWS Config, GuardDuty, Security Hub, and WAF provide layered controls.

## Performance
Fargate services scale on CPU and request load. CloudFront caches static/edge-cacheable content. Database capacity is monitored using CPU, connections, latency, free storage, and Performance Insights.

## Cost
The architecture begins with conservative baseline capacity, then uses metrics for rightsizing. Savings Plans or Reserved Instances are evaluated only after stable usage patterns exist.

## Operations
All production resources carry `Environment`, `Owner`, `Application`, `CostCenter`, `ManagedBy`, and `DataClassification` tags. Alerts are routed by severity and linked to runbook actions.
