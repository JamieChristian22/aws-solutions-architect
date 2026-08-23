# ADR-003 — Warm-Standby Regional DR

**Status:** Accepted

## Decision
Use `us-east-1` as primary and `us-west-2` as DR. Replicate durable object data, copy database snapshots cross-region, retain Terraform for regional rebuild, and keep DNS failover procedures documented.

## Why Not Active/Active
The business RTO is 60 minutes and RPO is 15 minutes. Full active/active would add substantial database consistency, routing, testing, and cost complexity not justified by the objective.

## Recovery Target
- RTO: 60 minutes
- RPO: 15 minutes transactional target
- Restore-test cadence: quarterly
