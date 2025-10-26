# ☁️ AWS Solutions Architect Portfolio

**Multi-Domain Cloud Architecture • Data & IoT Solutions • Serverless Engineering • FinOps**

This portfolio showcases AWS end-to-end architectures I’ve designed and implemented — each following **AWS Well-Architected Framework pillars** (Security, Reliability, Performance Efficiency, Cost Optimization, Operational Excellence).  
All projects are **production-grade**, **cost-aware**, and **documented with IaC**, architecture diagrams, and service breakdowns.

---

## 🚀 Featured Projects

### 🛒 1. Retail Analytics Platform
**Goal:** Enable real-time retail insights and personalization using serverless analytics.  
**Key AWS Services:** S3 Data Lake, Lambda, Glue, Athena, Redshift Serverless, QuickSight, API Gateway, CloudWatch.  
**Highlights:**
- Serverless event ingestion and ETL pipeline  
- Lakehouse architecture for BI dashboards  
- FinOps tagging and cost monitoring  
📂 [`/retail-analytics-platform`](retail-analytics-platform)

---

### 📊 2. Clickstream Analytics System
**Goal:** Capture, process, and analyze user interactions (clicks, sessions, paths) for real-time behavioral insights.  
**Architecture:**
- API Gateway → Lambda → SQS/Kinesis → S3 (raw → curated)  
- Glue Catalog + Athena queries  
- QuickSight dashboards for behavioral funnels  
**Focus:** Event-driven ingestion, lightweight transformation, analytics at scale.  
📂 [`/clickstream-analytics`](clickstream-analytics)

---

### 🩺 3. Healthcare Data Platform
**Goal:** Build a secure, HIPAA-style data platform for medical data ingestion, storage, and analytics.  
**AWS Stack:** S3 (PHI segregation zones), Glue, Athena, Redshift, CloudTrail, KMS, IAM, GuardDuty, Security Hub.  
**Features:**
- PHI encryption in transit and at rest  
- Access logging and audit compliance  
- Curated data layers for analytics  
📂 [`/healthcare-data-platform`](healthcare-data-platform)

---

### 🌐 4. IoT Sensor Analytics System (Edge → Cloud)
**Goal:** Collect, process, and analyze IoT device telemetry data from edge to cloud in real time.  
**Flow:** IoT Core → Kinesis → Lambda → DynamoDB/S3 → QuickSight  
**Highlights:**
- Edge-to-cloud telemetry  
- Time-series metrics and anomaly detection  
- Secure device identity and MQTT communication  
📂 [`/iot-sensor-analytics`](iot-sensor-analytics)

---

## 🧩 AWS Services Across All Projects

| Category              | Core AWS Services Used |
|------------------------|------------------------|
| Compute & Serverless   | Lambda, Fargate, API Gateway, AppSync |
| Data & Analytics       | S3, Glue, Athena, Redshift, QuickSight, Kinesis |
| Storage & Databases    | DynamoDB, S3, RDS (Aurora) |
| Security & Governance  | IAM, KMS, WAF, GuardDuty, CloudTrail, Security Hub |
| Observability          | CloudWatch, X-Ray, SNS, Cost Anomaly Detection |
| Networking             | VPC, CloudFront, Route 53, PrivateLink |
| IaC & DevOps           | AWS CDK, CloudFormation, CodePipeline, CodeBuild |
| FinOps & Optimization  | Budgets, Cost Explorer, Tag Policies, Intelligent Tiering |

Each design balances **performance, scalability, and cost efficiency**, using AWS Free Tier or pay-as-you-go resources whenever possible.

---

## 💸 FinOps & Cost Optimization

| Environment | Est. Monthly Cost | Description |
|--------------|------------------|--------------|
| **Dev/Test** | \$25–\$50 | Lightweight deployments and demo data |
| **Prod (SMB)** | \$200–\$400 | Scaled workloads with observability |
| **Enterprise** | \$1K–\$1.5K | Full analytics stack with security & compliance |

Detailed cost modeling and tagging examples can be found in `/finops`.

---

## 📂 Repository Structure

```text
aws-solutions-architect/
├── clickstream-analytics/       # Event-driven analytics and real-time ingestion
├── healthcare-data-platform/    # Secure healthcare data ingestion and analytics
├── iot-sensor-analytics/        # IoT edge-to-cloud telemetry analytics
├── retail-analytics-platform/   # Serverless retail data lake and BI dashboards
├── architecture-diagrams/       # PNG / draw.io / PDF visuals for all projects
├── finops/                      # Cost management and tagging strategy
└── README.md                    # (this file)
