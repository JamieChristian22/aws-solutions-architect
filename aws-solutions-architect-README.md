<p align="center">
  <img src="banner.png" width="100%" alt="AWS Solutions Architect Banner"/>
</p>

# ☁️ AWS Solutions Architect Portfolio

**Cloud Architecture · Serverless Engineering · Data Analytics · FinOps**

This repository showcases **real-world AWS architecture projects** designed and implemented by **Jamie Christian II**, focusing on **serverless**, **event-driven**, and **data-centric** solutions aligned with the **AWS Well-Architected Framework**.  

Each project demonstrates **production-grade design**, **security best practices**, and **cost optimization strategies** — providing end-to-end architecture, infrastructure-as-code (IaC), documentation, and FinOps analysis.

---

## 🧱 Portfolio Projects

### 🛒 [Retail Analytics & Personalization Platform](./retail-analytics-platform/)
> **Purpose:** Build a serverless, event-driven retail analytics system for personalized recommendations and BI dashboards.  
> **Architecture:** API Gateway → Lambda → Kinesis → S3 Data Lake → Glue → Athena → Redshift Serverless → QuickSight.  
> **Highlights:**
> - Real-time event ingestion and transformation  
> - Data Lakehouse architecture using AWS Glue & Athena  
> - Redshift Serverless for analytics & QuickSight dashboards  
> - FinOps-driven design with cost transparency  
> - IaC via AWS CDK (TypeScript)

### 🧠 (Coming Soon) [Clickstream Analytics on AWS](./clickstream-analytics/)
> **Purpose:** Capture and analyze user behavior events using Kinesis, Lambda, S3, and QuickSight.  
> **Focus:** Real-time metrics dashboards, retention analysis, and user funnel insights.  

### 🏥 (Coming Soon) [Healthcare Data Ingestion Platform](./healthcare-data-platform/)
> **Purpose:** Secure data ingestion for healthcare systems following HIPAA compliance.  
> **Focus:** Security controls, encryption, data governance, and patient data analytics.

---

## 🏗️ High-Level Architecture Example
![AWS Retail Analytics Architecture Diagram](retail-analytics-platform/docs/AWS_Retail_Analytics_Architecture_Diagram.png)

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
| **DevOps & IaC** | AWS CDK, CodePipeline, CodeBuild, CloudFormation |
| **FinOps** | Budgets, Cost Explorer, Intelligent Tiering, Reserved Savings Plans |

---

## 💰 FinOps Overview

| Tier | Monthly Estimate | Description |
|------|------------------|--------------|
| **Dev / Demo** | $25 – $50 | Light workloads for prototyping & learning |
| **Startup Launch** | $200 – $400 | Active analytics & dashboards at small scale |
| **Scale-Up** | $1 K – $1.5 K | Enterprise-grade throughput and storage |

📊 Detailed sheet: [`finops/finops_cost_estimates.xlsx`](./finops/finops_cost_estimates.xlsx)

---

## 📈 Skills Demonstrated

| Area | Competencies |
|------|---------------|
| **Architecture Design** | Multi-account setup, high availability, DR patterns |
| **Data Engineering** | Lakehouse design, ETL pipelines, analytics queries |
| **Security** | IAM least privilege, encryption, threat detection, WAF tuning |
| **Observability** | Dashboards, alarms, traces, logging pipelines |
| **DevOps / IaC** | AWS CDK, CI/CD pipelines, versioned deployments |
| **FinOps** | Cost tagging, anomaly detection, optimization reports |

---

## 🧩 Repository Structure

```
aws-solutions-architect/
├── retail-analytics-platform/       ← Full project with CDK, Lambda, Glue, analytics
│   ├── README.md
│   ├── docs/
│   ├── cdk/
│   ├── services/
│   ├── analytics/
│   └── observability/
├── architecture-diagrams/           ← PNGs, PDFs, Draw.io files
│   └── AWS_Retail_Analytics_Architecture_Diagram.png
├── finops/                          ← Cost and FinOps documentation
│   ├── finops_cost_estimates.xlsx
│   └── finops_cost_estimates.csv
└── README.md                        ← (this file)
```

---

## 🧠 Learning Objectives
- Design and implement **serverless event-driven architectures**  
- Apply **AWS Well-Architected Framework** across all five pillars  
- Automate provisioning with **Infrastructure-as-Code (CDK)**  
- Integrate **security, observability, and cost optimization**  
- Present architectures with **enterprise documentation & diagrams**  

---

## 🪪 License
MIT License © 2025 **Jamie Christian II**

---

## 👤 Author
**Jamie Christian II**  
🧭 AWS Certified · Solutions Architect · Data & BI Analyst  
🔗 [LinkedIn](https://www.linkedin.com/in/jamiechristian22) | [GitHub](https://github.com/JamieChristian22)
