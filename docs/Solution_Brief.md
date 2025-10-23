# Solution Brief — Event-Driven Retail Analytics

**Problem:** Retailer needs real-time recommendations and daily KPIs with strong security, low ops burden, and DR.

**Approach:** Serverless, event-driven, data-lake-centric architecture with low-latency cache for personalization and curated analytics for BI.

**Why this design**
- **Agility & Cost:** Serverless (API Gateway, Lambda, Firehose, Athena, Redshift Serverless) scales to demand.
- **Quality & Insights:** Enrichment at ingest → curated lake → BI dashboards; schema-on-read and CTAS for speed.
- **Security-by-default:** KMS, WAF, least-privilege IAM, centralized logs, tagging standards.
- **Reliability:** S3 durability + partitioning; alarms, canaries; DR patterns (CRR, failover).

**KPIs (examples)**
- Conversion rate, AOV, GMV, funnel steps, session duration, cohort retention.

**Risks & Mitigations**
- **PII exposure** → Macie + lake zoning + column-level encryption.
- **Hot partitions** → Kinesis shard scaling; DDB adaptive capacity + keys.
- **Cost drift** → Budgets, cost allocation tags, lifecycle, Serverless scaling controls.
