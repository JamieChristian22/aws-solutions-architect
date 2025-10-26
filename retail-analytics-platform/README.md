# Retail Analytics Platform – Real-Time Sales, Inventory & Customer Insights on AWS

## 1. Business Problem
Retail leadership needs live visibility into sales, inventory risk, and customer buying behavior across 100+ stores. Traditional reporting is next-day Excel. That causes stockouts, overstock carrying cost, and missed revenue opportunities.

## 2. Solution Overview
This serverless, AWS-native Retail Analytics Platform:
- Ingests POS transactions, inventory scans, and loyalty events in near real time
- Cleans, standardizes, and enriches data
- Publishes executive dashboards for Revenue, Margin %, Basket Size, and Inventory Risk
- Pushes proactive low-stock alerts to store managers via SNS

Latency: minutes, not next day.

## 3. High-Level Architecture
Flow:  
Store Systems → API Gateway → Lambda → Kinesis Data Streams → S3 Data Lake (raw/staged/curated) → Glue ETL → Redshift Serverless → QuickSight Dashboards + SNS Alerts.

See diagrams:
- `diagrams/Retail_Analytics_Architecture.png`
- `diagrams/Data_Flow_Pipeline.png`

### Core AWS Services
- **Amazon API Gateway / AWS Lambda / Amazon Kinesis Data Streams** – Real-time ingestion
- **Amazon S3 (raw/staged/curated zones)** – Durable data lake
- **AWS Glue (ETL + Data Catalog)** – Batch transformation, schema management
- **Amazon Athena** – Ad hoc SQL on curated S3 data
- **Amazon Redshift Serverless** – Star schema warehouse for BI
- **Amazon QuickSight** – Executive dashboards
- **Amazon SNS** – Automated low-stock alerts
- **IAM, KMS, Lake Formation, CloudTrail, CloudWatch** – Security, governance, audit, monitoring

## 4. Data Model (Analytics Layer)
Redshift Serverless is modeled as a star schema.

### Dimensions
- `dim_store` (store_id, region, manager, timezone)
- `dim_product` (sku, category, cost, brand)
- `dim_calendar` (date_key, day_of_week, week_num, fiscal_period)

### Facts
- `fact_sales` (timestamp_utc, store_id, sku, qty_sold, unit_price, gross_margin, basket_id)
- `fact_inventory_snapshot` (timestamp_utc, store_id, sku, on_hand_qty, reorder_point, risk_flag)

## 5. Dashboards
- **Store Performance Dashboard**
  - Revenue Today vs Target
  - Avg Basket Size
  - Gross Margin %
  - Regional Heatmap
- **Inventory Risk Dashboard**
  - Low-stock SKUs
  - Overstock SKUs
  - Inventory Turns
- **Customer Behavior Dashboard**
  - Attach Rate (bought together)
  - Loyalty Spend per Visit
  - Top Cross-Sell Pairs

## 6. Cost & Security
- Serverless-first (Lambda, Kinesis, Glue, Athena, Redshift Serverless autoscale)
- S3 is source of truth; historical data ages to Glacier
- KMS encryption at rest, TLS in transit
- Lake Formation + row-level security → store managers only see their stores

See `docs/Cost_Security_Notes.md`.

## 7. Operations / Monitoring
- CloudWatch alarms on Lambda error rate, Kinesis throughput, Glue job failures
- CloudTrail audit logging for governance
- SNS alerts for low-stock events to Store Ops leadership

See `docs/Executive_Summary.md` for the business story you tell in interviews.
