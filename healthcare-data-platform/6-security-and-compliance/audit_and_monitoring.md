# Audit and Monitoring

## CloudTrail
- Captures every API call / console access related to PHI data in S3, Glue, Athena, Lambda.
- Logs are stored in a dedicated audit bucket with MFA delete.

## CloudWatch
- Monitors Lambda error rates (alert logic failures).
- Monitors Glue ETL job success/failure.
- Alarms notify engineering if risk scoring fails to run.

## AWS Config
- Ensures buckets are encrypted, public access is blocked, and versioning is on.
- Noncompliant resources raise findings.

## Amazon Macie (Optional)
- Scans S3 buckets for sensitive data and flags if PHI ends up in the wrong zone (e.g. analytics/).