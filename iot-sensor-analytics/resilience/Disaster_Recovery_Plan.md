# Disaster Recovery
Primary us-east-1, recovery us-west-2. RTO 60 minutes, RPO ≤5 minutes for accepted stream/lake data. Replicate S3 for DR-class deployment and recreate IoT rules, Kinesis, Lambda, Firehose, Glue, SNS, and observability from CDK. Validate recovery endpoint, telemetry processing, alerting, and lake delivery before cutover.
