# 🏥 Healthcare Data Platform on AWS — Secure Analytics Architecture

A regulated-data architecture portfolio demonstrating **secure ingestion, de-identification, governed data lake, analytics, auditability, resilience, IaC, and cost governance**.

> This is a simulated healthcare architecture. It demonstrates HIPAA-aligned technical patterns but does not claim certification or that AWS services alone create compliance.

## Scenario
Patients represented: 500,000
Daily clinical/operational records: 2,500,000
Average record: 2.2 KB
Raw daily ingestion: ~5.50 GB
Availability target: 99.9%
RTO: 4 hours
RPO: 15 minutes

## Architecture
Sources → API/SFTP ingestion → encrypted landing S3 → Glue/Lambda de-identification → curated S3 Parquet → Lake Formation/Glue Catalog → Athena/Redshift Serverless → QuickSight.

Security services: IAM Identity Center, KMS, CloudTrail, Config, GuardDuty, Security Hub, Macie, VPC endpoints.

## Security Principles
Minimum necessary access • PHI segregation • encryption • immutable audit trail • private data services • de-identification before broad analytics • documented retention/deletion.

## Modeled FinOps
Baseline $18,400/month; optimization backlog $3,150/month; modeled reduction 17.1%. Planning assumptions only.

## Verification Evidence

The `evidence/` folder provides additional review-ready artifacts that demonstrate traceability, control validation, operational acceptance, and modeled test evidence. Any benchmark, cost, DR, or execution result that was not run against a live AWS account is explicitly labeled as **simulated**, **modeled**, or **planning evidence** rather than presented as production proof.

