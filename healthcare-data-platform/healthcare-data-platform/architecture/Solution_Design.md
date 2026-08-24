# Solution Design

## Zones
Landing: encrypted source copies, tightly restricted.
Quarantine: failed validation / suspected sensitive-data issues.
Curated: de-identified Parquet.
Analytics: governed views/data products.

## Access
Analysts do not query raw PHI by default. Lake Formation grants database/table/column permissions. Sensitive workflows require dedicated roles.

## Networking
Private subnets and VPC endpoints for S3/KMS/Glue where appropriate. No public database endpoints.

## Logging
CloudTrail, S3 access logs, Lake Formation access events, Security Hub findings, Macie findings.
