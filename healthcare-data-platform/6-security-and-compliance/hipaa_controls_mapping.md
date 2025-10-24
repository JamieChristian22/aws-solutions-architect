# HIPAA Controls Mapping (Technical Safeguards Focus)

## Access Control
- IAM roles are scoped per data zone:
  - raw/: only ETL + compliance
  - curated/: data engineering + clinical analytics
  - analytics/: leadership dashboards (minimized PHI)
- QuickSight row-level security limits PHI visibility by facility.

## Audit Controls
- AWS CloudTrail logs all access to S3, Glue, Athena, Kinesis, Lambda.
- CloudWatch logs ETL pipeline runs and Lambda alert logic.

## Integrity
- S3 versioning is enabled for raw data buckets to preserve original clinical records.
- Glue jobs write immutable curated datasets (no in-place mutation).

## Transmission Security
- All ingestion via TLS (SFTP on Transfer Family, API Gateway HTTPS).
- VPC endpoints for S3/Glue/Athena keep PHI off the public internet path.

## Encryption
- AWS KMS CMK encrypts data at rest in S3, Glue bookmarks, Athena query results.
- TLS enforces encryption in transit.

This design uses only HIPAA-eligible AWS services and is intended to run under a BAA.