# DR Plan
RTO 2 hours, RPO 15 minutes. S3 is durable analytical truth. Replicate critical data to secondary region for DR-class deployment. Recreate Glue/Lake Formation/Redshift/QuickSight datasets from IaC/config exports. Validate data counts and latest partition before BI cutover.
