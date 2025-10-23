**☁️ AWS Solutions Architect Portfolio**

**Cloud Architecture · Serverless Engineering · Data Analytics · FinOps**

Welcome to my **AWS Solutions Architect portfolio** — a collection of **real-world AWS architecture projects** built while completing the **AWS Certified Solutions Architect – Associate Exam Prep** course.  

These projects demonstrate applied knowledge in **cloud design, data pipelines, and serverless architecture**, following the **AWS Well-Architected Framework** and emphasizing **security**, **reliability**, **cost optimization**, and **performance efficiency**.

---

## 🧱 Featured Project

### 🛒 [Retail Analytics & Personalization Platform](./retail-analytics-platform/)
> **Purpose:** Design and deploy a real-time, event-driven analytics and recommendation system for a retail business.  
> **Architecture:** API Gateway → Lambda → Kinesis → S3 Data Lake → Glue → Athena → Redshift Serverless → QuickSight.  
> **Highlights:**
> - Serverless ingestion and transformation pipeline  
> - Data Lakehouse built with S3, Glue, and Athena  
> - Redshift Serverless for analytics & QuickSight dashboards  
> - FinOps-optimized design with cost visibility  
> - Infrastructure deployed via AWS CDK (TypeScript)

---

## 🏗️ High-Level Architecture

![AWS Retail Analytics Architecture Diagram](https://raw.githubusercontent.com/JamieChristian22/aws-solutions-architect/main/retail-analytics-platform/docs/AWS_Retail_Analytics_Architecture_Diagram.png)

---

## ⚙️ Core AWS Services Demonstrated

| Category | Services |
|-----------|-----------|
| **Compute & API** | Lambda, API Gateway, AppSync, Fargate |
| **Data & Analytics** | Kinesis, Glue, Athena, Redshift Serverless, QuickSight |
| **Storage** | S3 (raw / curated / archive), DynamoDB |
| **Security & Compliance** | IAM, KMS, WAF, GuardDuty, Security Hub, Macie |
| **Networking & Delivery** | CloudFront, Route 53, VPC, PrivateLink |
| **Observability** | CloudWatch, X-Ray, SNS, Budgets, Anomaly Detection |
| **DevOps / IaC** | AWS CDK, CodePipeline, CodeBuild, CloudFormation |
| **FinOps** | Budgets, Cost Explorer, Intelligent Tiering, Reserved Savings Plans |

---

## 💰 FinOps Overview

| Tier | Monthly Estimate | Description |
|------|------------------|--------------|
| **Dev / Demo** | $25 – $50 | Lightweight workloads for prototyping & testing |
| **Startup Launch** | $200 – $400 | Moderate-scale analytics and dashboards |
| **Scale-Up** | $1 K – $1.5 K | Enterprise-grade, production-level deployment |

📊 Full details: [`finops/finops_cost_estimates.xlsx`](./finops/finops_cost_estimates.xlsx)

---

## 🧠 Skills Demonstrated

| Area | Competencies |
|------|---------------|
| **Architecture Design** | Multi-account setup, high availability, DR patterns |
| **Data Engineering** | ETL, Lakehouse design, Athena queries |
| **Security** | IAM least privilege, encryption, WAF protection |
| **Observability** | CloudWatch dashboards, logs, and alarms |
| **DevOps / IaC** | AWS CDK, CI/CD automation, stack modularity |
| **FinOps** | Cost monitoring, tagging, optimization strategies |

---

## 🧩 Repository Structure

```
aws-solutions-architect/
├── retail-analytics-platform/       ← Full AWS architecture project
│   ├── README.md
│   ├── docs/
│   ├── cdk/
│   ├── services/
│   ├── analytics/
│   └── observability/
├── architecture-diagrams/           ← PNGs, PDFs, Draw.io files
│   └── AWS_Retail_Analytics_Architecture_Diagram.png
├── finops/                          ← Cost analysis documentation
│   ├── finops_cost_estimates.xlsx
│   └── finops_cost_estimates.csv
└── README.md                        ← (this file)
```

---

## 🧩 Upcoming Projects
- 🧠 **Clickstream Analytics on AWS** — Real-time user behavior pipelines  
- 🏥 **Healthcare Data Platform** — HIPAA-compliant ingestion & analysis  
- ⚙️ **IoT Sensor Analytics System** — Edge-to-cloud telemetry on AWS  

---

## 🪪 License
MIT License © 2025 **Jamie Christian II**

---

## 👤 Author
**Jamie Christian II**  
🧭 *AWS Solutions Architect (Associate-Level Exam Prep)* · *Data & BI Analyst*  
🔗 [LinkedIn](https://www.linkedin.com/in/jamiechristian22) | [GitHub](https://github.com/JamieChristian22)
