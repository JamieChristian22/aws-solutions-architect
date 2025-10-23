# Event-Driven Retail Analytics & Personalization (AWS, Multi-Account-Ready)

Production-grade reference implementation you can demo in minutes: a secure, serverless, event-driven analytics + recommendations stack with IaC, CI/CD, observability, and DR.

## TL;DR Demo
1. **Deploy** the CDK app to your dev account.
2. **Send events** to API Gateway (product_view, add_to_cart, purchase).
3. **Query** data in Athena/Redshift Serverless; **view** QuickSight KPIs.
4. **Hit** `/recommendations` endpoint to fetch cached personalized recs.
5. **Trigger** a synthetic alarm → verify notifications (SNS/email/Slack).

> This repo is intentionally scoped for quick deployment but structured like a real engagement. Expand modules as needed.

---

## Architecture (High Level)

```mermaid
flowchart LR
  subgraph Client["Web / Mobile Client"]
    A[SPA / App] -->|Auth| COG[Cognito]
    A -->|HTTPS JSON| API[API Gateway + WAF]
  end

  API --> KDS[Kinesis Data Streams]
  KDS --> L1[Lambda Transform/Enrich]
  L1 --> FHZ[Firehose]
  FHZ --> S3_RAW[(S3 Data Lake<br/>raw/)]
  S3_RAW --> GLUE[Glue Crawler/ETL]
  GLUE --> S3_CUR[(S3 curated/)]
  S3_CUR --> ATH[Athena SQL]
  S3_CUR --> RS[Redshift Serverless]
  RS --> QS[QuickSight Dashboards]

  L1 --> DDB[(DynamoDB Profiles/Recs Cache)]
  DDB --> L2[Lambda Recs API]
  L2 --> API

  subgraph Edge
    WAF[WAF] --> CF[CloudFront] --> Static[SPA Hosting (S3)]
  end

  subgraph SecOps
    CT[CloudTrail] --> S3_LOGS[(S3 Log Archive)]
    GU[GuardDuty] --> SH[Security Hub]
    CW[CloudWatch + X-Ray] --> ALR[Alarms/Canaries]
  end
```

**Key Choices**
- **Serverless-first** to minimize ops and cost.
- **Data lake centric** with curated layers → Athena & Redshift.
- **DynamoDB** for low-latency personalization cache.
- **WAF, KMS, IAM least-privilege, centralized logs** for security.
- **S3 CRR + Route 53 failover** patterns to support DR.

---

## Repo Structure
```
aws-retail-analytics/
├─ cdk/                       # AWS CDK (TypeScript) stacks and pipelines
│  ├─ bin/                    # Entrypoints per env (dev/prod)
│  ├─ lib/                    # Stacks: network, data, app, analytics
│  ├─ pipelines/              # (Optional) CodePipeline definitions
│  ├─ package.json            # CDK app deps & scripts
│  └─ tsconfig.json
├─ services/
│  ├─ ingest-api/             # API Gateway + Lambda (ingestion)
│  ├─ stream-processing/      # Lambda consumer (transform/enrich)
│  └─ recommenders/           # Recs API (reads DynamoDB cache)
├─ analytics/
│  ├─ glue-jobs/              # PySpark ETL skeleton
│  ├─ athena-sql/             # DDL/DML for tables & views
│  └─ redshift/               # Star schema SQL
├─ observability/
│  ├─ dashboards/             # CloudWatch dashboards (JSON)
│  └─ runbooks/               # Incident & DR runbooks
└─ docs/
   ├─ Solution_Brief.md
   ├─ Well_Architected.md
   └─ Threat_Model.md
```

---

## Quickstart

### Prereqs
- Node 18+, npm, AWS CLI configured, CDK v2 (`npm i -g aws-cdk`).
- An AWS account + IAM role with permissions to deploy CDK (dev environment).

### Install & Bootstrap
```bash
cd cdk
npm install
cdk bootstrap
```

### Deploy (dev)
```bash
cdk deploy --all
```

### Send Sample Events
```bash
# Replace with your API endpoint from the CDK output
API="https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/events"

curl -X POST "$API" -H "Content-Type: application/json" -d '{
  "event":"product_view",
  "user_id":"u-123",
  "session_id":"s-abc",
  "sku":"SKU-001",
  "price":19.99,
  "ts":"2025-10-22T12:00:00Z"
}'
```

### Query in Athena
- Database: `retail_analytics`
- Table: `events_raw`
- Example (daily purchases):
```sql
SELECT date(ts) AS day, count(*) purchases
FROM retail_analytics.events_raw
WHERE event = 'purchase'
GROUP BY 1 ORDER BY 1 DESC;
```

---

## Next Steps / Extensions
- Add **OpenSearch Serverless** for full-text product search.
- Swap recommender to **Amazon Personalize** or **SageMaker** inference.
- Add **multi-account** CI/CD with cross-account `AssumeRole` in `pipelines/`.
- Enable **S3 CRR**, **DynamoDB global tables**, and **Route 53** health checks.
- Turn on **Macie** for PII detection in lake, plus **Security Hub** standards.
```

---

## License
MIT
