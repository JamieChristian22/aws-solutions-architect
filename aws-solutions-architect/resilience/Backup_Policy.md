# Backup Policy

## RDS
- automated backups enabled
- 14-day operational retention target
- deletion protection in production
- cross-region copy for disaster-recovery requirement
- quarterly restore validation

## S3
- versioning enabled for critical buckets
- lifecycle moves older noncurrent versions/log objects to lower-cost storage where appropriate
- replication reserved for data classified as DR-critical

## Configuration
Terraform source is version-controlled. Secrets are not stored in Git. Configuration recovery is tested with environment rebuilds.
