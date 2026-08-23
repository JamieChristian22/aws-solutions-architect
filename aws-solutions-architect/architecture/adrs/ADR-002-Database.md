# ADR-002 — Use RDS PostgreSQL Multi-AZ

**Status:** Accepted

## Decision
Use Amazon RDS for PostgreSQL with Multi-AZ deployment, encryption, automated backups, Performance Insights, and deletion protection in production.

## Rationale
The workload requires relational transactions and a 15-minute RPO. Managed RDS reduces operational burden and supports automated failover.

## Tradeoffs
Managed service cost is higher than a single self-managed instance, but the architecture buys automated failover, backup integration, monitoring, and lower administrative risk.
