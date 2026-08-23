# Terraform Deployment Guide

## What It Builds
Two-AZ VPC, public/app/database subnets, per-AZ NAT gateways, security groups, KMS key, encrypted log bucket, ECS/Fargate service, ALB, RDS PostgreSQL Multi-AZ, CloudWatch alarms, and SNS alert topic.

## Commands
```bash
terraform init
terraform fmt -check -recursive
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```

## State
For a real deployment, configure an encrypted remote S3 backend with DynamoDB/state locking or the organization's approved Terraform state platform. Backend configuration is intentionally environment-specific and should not contain credentials in Git.

## Production Safety
The RDS resource has deletion protection and requires a final snapshot. Production apply should occur only through the protected CI environment.
