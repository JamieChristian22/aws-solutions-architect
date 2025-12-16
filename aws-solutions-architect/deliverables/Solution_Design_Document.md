# Solution Design Document (SDD)

## Business Context
Client requires a secure, scalable AWS environment supporting growth, compliance, and cost efficiency.

## Requirements
- High availability
- Least-privilege IAM
- Centralized logging & monitoring
- Cost visibility and optimization

## Proposed Architecture
- VPC with public/private subnets
- ALB + Auto Scaling
- IAM roles and policies
- CloudWatch, CloudTrail, GuardDuty

## Risks & Mitigations
- Misconfigured IAM → policy boundaries + reviews
- Cost overruns → budgets & alerts
