# 🛒 AWS Retail Analytics & Personalization Platform  
**Event-Driven · Serverless · Scalable · FinOps-Aligned**

---

## 📖 Case Study Overview

### 🎯 Business Challenge  
A mid-sized retail company needed to **modernize its analytics pipeline** to support:
- Real-time tracking of customer activity  
- Personalized product recommendations  
- Centralized data storage for BI and forecasting  
- Reduced infrastructure costs and operational complexity  

Their legacy on-prem system relied on batch ETL jobs, which caused **data delays**, **high costs**, and **limited scalability**.  

---

### 💡 Solution Overview  
As the AWS Solutions Architect, I designed a **serverless, event-driven analytics and personalization platform** using **AWS managed services**.  

The solution enables real-time event ingestion, transformation, and reporting — with **zero servers to manage** and **pay-per-use efficiency**.  

---

## 🏗️ High-Level Architecture
![AWS Retail Analytics Architecture Diagram](https://github.com/JamieChristian22/aws-solutions-architect/blob/main/retail-analytics-platform/docs/AWS_Retail_Analytics_Architecture_Diagram.png?raw=true)

**Data Flow:**
1. **Customer actions** (product views, cart adds, purchases) are sent via **API Gateway** to **Lambda** functions.  
2. Events are streamed through **Kinesis Data Streams** → **Firehose** → **S3 Data Lake (raw layer)**.  
3. **AWS Glue** crawlers detect schema and ETL jobs transform data to a curated layer.  
4. **Athena** and **Redshift Serverless** query curated data for KPIs, dashboards, and ML model retraining.  
5. **QuickSight** provides visual dashboards for executives and analysts.  
6. **DynamoDB** stores personalized recommendations served via **API Gateway**.  

**Data Flow:**
1. **Customer actions** (product views, cart adds, purchases) are sent via **API Gateway** to **Lambda** functions.  
2. Events are streamed through **Kinesis Data Streams** → **Firehose** → **S3 Data Lake (raw layer)**.  
3. **AWS Glue** crawlers detect schema and ETL jobs transform data to a curated layer.  
4. **Athena** and **Redshift Serverless** query curated data for KPIs, dashboards, and ML model retraining.  
5. **QuickSight** provides visual dashboards for executives and analysts.  
6. **DynamoDB** stores personalized recommendations served via **API Gateway**.  

---

## ⚙️ AWS Services Used

| Layer | Services | Purpose |
|-------|-----------|----------|
| **Edge & Security** | CloudFront, WAF, Route 53 | Protect and deliver APIs and static content |
| **Compute & API** | Lambda, API Gateway | Event ingestion and transformation |
| **Streaming** | Kinesis Data Streams, Kinesis Firehose | Real-time data ingestion to S3 |
| **Storage / Lake** | Amazon S3 (raw, curated), DynamoDB | Centralized data lake and low-latency store |
| **ETL & Analytics** | Glue, Athena, Redshift Serverless | Schema detection, transformation, BI queries |
| **Visualization** | QuickSight | Business KPIs, revenue, and behavior dashboards |
| **Observability** | CloudWatch, X-Ray, GuardDuty | Logs, traces, and security monitoring |
| **Infrastructure-as-Code** | AWS CDK (TypeScript) | Automated provisioning and deployment |
| **FinOps** | AWS Budgets, Cost Explorer | Cost control and optimization reporting |

---

## 💰 Cost & Scalability
| Tier | Monthly Estimate | Description |
|------|------------------|--------------|
| **Dev / Demo** | $25 – $50 | Minimal usage for testing or training |
| **Startup Launch** | $200 – $400 | Steady data flow, dashboards, and small team |
| **Scale-Up / Enterprise** | $1 K – $1.5 K | High-volume data ingestion and BI workloads |

**FinOps Highlights:**
- Intelligent-Tiering for S3 data storage  
- On-demand Lambda execution (no idle cost)  
- Redshift Serverless scaling on query demand  
- Kinesis shard scaling policies for elasticity  

---

## 🔐 Security & Compliance
- IAM least-privilege roles for all resources  
- S3 bucket policies with KMS encryption (AES-256)  
- TLS 1.2 enforced on all data transfer endpoints  
- WAF managed rules for API protection  
- GuardDuty & Security Hub for continuous threat detection  
- Macie scans for PII compliance  

---

## 📊 Observability & Reliability
- **CloudWatch Dashboards:** API latency, Lambda errors, Kinesis metrics  
- **X-Ray Tracing:** End-to-end visibility into event flows  
- **SNS Alerts:** Error and performance anomaly notifications  
- **Incident Runbook:** Defined recovery procedures with RTO/RPO metrics  

---

## 🧠 Business Outcomes
✅ Reduced data latency from **hours to seconds**  
✅ Enabled **personalized product recommendations** in real time  
✅ Decreased infrastructure costs by **~60%**  
✅ Delivered **daily BI dashboards** for leadership using QuickSight  
✅ Improved scalability and availability with serverless design  

---

## 🧩 Learning Outcomes
This case study demonstrates:
- Designing **event-driven AWS architectures** with serverless patterns  
- Applying the **Well-Architected Framework** pillars in real-world projects  
- Automating provisioning with **AWS CDK**  
- Integrating analytics, observability, and FinOps in a single ecosystem  

---

## 🪪 License
MIT License © 2025 **Jamie Christian II**

---

## 👤 Author
**Jamie Christian II**  
🧭 *AWS Solutions Architect (Associate-Level Exam Prep)* · *Data & BI Analyst*  
🔗 [LinkedIn](https://www.linkedin.com/in/jamiechristian22) | [GitHub](https://github.com/JamieChristian22)
