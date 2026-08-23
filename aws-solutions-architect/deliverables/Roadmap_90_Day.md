# 90-Day Cloud Optimization Roadmap

## Days 1–30 — Assess and Establish the Foundation
- conduct discovery workshop
- inventory workloads, data classifications, owners, and dependencies
- complete Well-Architected review
- agree RTO/RPO and availability targets
- establish Terraform remote-state pattern
- define network CIDRs and security boundaries
- implement tagging standard and budget ownership
- establish CI validation pipeline

**Exit criteria:** approved architecture, traceable requirements, risk register, Terraform foundation, and delivery backlog.

## Days 31–60 — Build and Harden
- deploy two-AZ VPC and private workload subnets
- deploy ALB and ECS/Fargate baseline
- deploy RDS Multi-AZ with encryption and backup controls
- enable CloudTrail, Config, GuardDuty, Security Hub
- implement WAF and IAM least-privilege patterns
- configure CloudWatch dashboards and alarms
- execute first cost review and rightsizing baseline

**Exit criteria:** pre-production platform passes security, network, and functional validation.

## Days 61–90 — Recover, Optimize, and Hand Off
- execute AZ-failure test
- execute regional recovery tabletop and restore exercise
- tune alarm thresholds
- complete FinOps savings backlog
- finalize operations runbook
- conduct knowledge transfer
- complete production-readiness review
- obtain acceptance sign-off

**Exit criteria:** tested recovery, operational ownership, approved residual risks, handoff complete.
