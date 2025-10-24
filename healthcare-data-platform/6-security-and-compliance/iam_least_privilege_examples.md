# IAM Least Privilege Examples

## Persona: Data Engineer
- Can read from raw/ and curated/
- Can run Glue jobs
- Cannot access QuickSight dashboards with PHI

## Persona: Care Coordinator
- Can view QuickSight dashboard filtered to their facility
- Cannot access raw/ S3 buckets
- Cannot run Athena queries directly

## Persona: Compliance / Audit
- Read-only access to CloudTrail logs
- Can verify PHI access attempts
- Cannot modify Glue jobs or Lambda logic

## Sample Policy Fragment (Curated-Only Read)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowReadCurated",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::hcp-curated-zone",
        "arn:aws:s3:::hcp-curated-zone/*"
      ]
    }
  ]
}