# 🧠 Real-Time Clickstream Analytics on AWS (Python) — v3

**All-Python stack**: AWS CDK (Python), Lambda (Python 3.11), API Gateway + WAF, Kinesis, Lambda Stream Processor → **dual-write** to **Firehose→S3 (Parquet)** and **OpenSearch (Cognito Dashboards)**, Glue/Athena, VPC Endpoints, KMS, IAM.

## Deploy
```bash
cd clickstream-analytics-py-v3/cdk
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
npm i -g aws-cdk@2
cdk bootstrap
cdk deploy
```
**Outputs**: `ApiUrl`, `KinesisStreamName`, `ProcessedBucketName`, `OpenSearchEndpoint`, `CognitoUserPoolId`, `CognitoIdentityPoolId`.

## Near‑Real‑Time Search
The Stream Processor dual‑writes:
- **Firehose → S3 (Parquet)** for the data lake
- **Bulk → OpenSearch** using credentials from **Secrets Manager** (master user created by CDK)
Environment:
- `OS_ENDPOINT` (CDK output wiring)
- `OS_SECRET_ARN` (Secrets Manager ARN)
- `OS_INDEX` (default `clickstream-events`)

## Quick test
```bash
cd clients/generator
pip install -r requirements.txt
API_URL=https://YOUR_API/prod/events python send_events.py
```
