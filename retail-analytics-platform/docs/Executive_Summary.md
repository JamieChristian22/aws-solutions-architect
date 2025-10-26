# Executive Summary

The Retail Analytics Platform delivers near real-time sales, margin, and inventory visibility across all stores.

## Problem
- Leadership received stale, next-day spreadsheets.
- Stores overstock slow SKUs and run out of fast movers.
- No automated alerting for low inventory.

## Solution
We built an AWS-native data platform that:
1. Streams POS and inventory events through API Gateway, Lambda, and Kinesis.
2. Lands all events in an S3 data lake (raw/staged/curated).
3. Uses Glue ETL to join transactions, inventory, and product master data.
4. Loads a star schema in Redshift Serverless for BI.
5. Publishes dashboards in QuickSight and sends proactive low-stock alerts via SNS.

## Business Impact
- Reduced stockouts: managers get alerts before shelves go empty.
- Lower carrying cost: identify overstock and rebalance between stores.
- Faster decisioning: executives see revenue, margin %, and sell-through in minutes instead of waiting until tomorrow.
