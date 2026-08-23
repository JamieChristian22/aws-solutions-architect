# ADR-001 — Use ECS on AWS Fargate

**Status:** Accepted

## Context
The SaaS workload is containerized, has variable traffic, and the customer does not want to operate EC2 worker fleets or Kubernetes control-plane complexity.

## Decision
Run the application on Amazon ECS using Fargate in private subnets across two Availability Zones.

## Consequences
**Benefits:** no host patching, task-level scaling, IAM task roles, simple ALB integration, reduced operational load.

**Tradeoffs:** less low-level host control and potentially higher unit cost than heavily optimized EC2 at sustained scale.

## Revisit Trigger
Re-evaluate if sustained compute spend exceeds the modeled Fargate baseline by 25% for three consecutive months or platform requirements justify EKS.
