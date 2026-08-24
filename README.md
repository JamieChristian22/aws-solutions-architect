# ☁️ AWS Solutions Architect Portfolio

![AWS](https://img.shields.io/badge/AWS-Solutions%20Architecture-232F3E?logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-Architecture%20Automation-3776AB?logo=python&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-Infrastructure%20as%20Code-844FBA?logo=terraform&logoColor=white)
![CDK](https://img.shields.io/badge/AWS-CDK-FF9900)
![Security](https://img.shields.io/badge/Security-Defense%20in%20Depth-success)
![FinOps](https://img.shields.io/badge/FinOps-Cloud%20Economics-blue)
![Status](https://img.shields.io/badge/Status-Portfolio%20Ready-brightgreen)

> **AWS Solutions Architecture • Cloud Consulting • Security • FinOps • Data Platforms • Event-Driven Systems • Infrastructure as Code**

A comprehensive AWS Solutions Architect portfolio demonstrating how business requirements can be translated into **secure, resilient, scalable, observable, cost-aware AWS architectures**.

This repository goes beyond basic AWS labs.

It demonstrates the complete architecture lifecycle:

**Discovery → Requirements → Architecture → Security → Infrastructure as Code → CI/CD → Observability → Reliability → Disaster Recovery → FinOps → Validation → Operational Handoff**

---

# 👤 Portfolio Focus

This repository is built around the work expected from:

- AWS Solutions Architects
- Associate / Junior Solutions Architects
- Cloud Solutions Architects
- Cloud Consultants
- AWS Professional Services Engineers
- Cloud Infrastructure Engineers
- Cloud Platform Engineers
- Technical Cloud Consultants

The portfolio demonstrates both:

### Technical Architecture

```text
AWS Services
Networking
Security
Data
Streaming
Serverless
Infrastructure as Code
Observability
Disaster Recovery
```

and:

### Customer-Facing Architecture

```text
Discovery
Requirements
Architecture Decisions
Risk Management
Cost Modeling
LOE Estimation
Roadmaps
Executive Communication
Knowledge Transfer
```

---

# 🧭 Start Here

| Project | Primary Focus | Architecture Depth |
|---|---|---:|
| **AWS Professional Services Portfolio** | Complete customer architecture engagement | ⭐⭐⭐⭐⭐ |
| **Clickstream Analytics** | High-volume event-driven architecture | ⭐⭐⭐⭐⭐ |
| **IoT Sensor Analytics** | Secure MQTT telemetry and anomaly detection | ⭐⭐⭐⭐⭐ |
| **Healthcare Data Platform** | Regulated-data security and governance | ⭐⭐⭐⭐⭐ |
| **Retail Analytics Platform** | Enterprise retail analytics and BI | ⭐⭐⭐⭐⭐ |
| **FinOps Framework** | Cloud financial management | ⭐⭐⭐⭐⭐ |
| **Consulting Toolkit** | Discovery, assessments, delivery and handoff | ⭐⭐⭐⭐⭐ |

---

# 📁 Repository Navigation

## 🧑‍💼 AWS Professional Services Portfolio

[`aws-solutions-architect/`](aws-solutions-architect/)

A complete customer-facing professional-services architecture engagement.

Demonstrates:

- Customer discovery
- Requirements traceability
- Architecture design
- Architecture Decision Records
- Terraform
- CI/CD
- IAM
- Threat modeling
- AWS Well-Architected
- Observability
- FinOps
- Disaster recovery
- Operations
- Knowledge transfer

### Architecture Scenario

```text
Route 53
   ↓
CloudFront
   ↓
AWS WAF
   ↓
Application Load Balancer
   ↓
ECS / Fargate
   ↓
RDS PostgreSQL Multi-AZ
```

Supporting services include:

```text
S3
KMS
CloudTrail
AWS Config
GuardDuty
Security Hub
CloudWatch
SNS
Terraform
GitHub Actions
```

### Reliability Targets

```text
Availability: 99.9%
RTO: 60 minutes
RPO: 15 minutes
```

This project demonstrates how architecture moves from:

**business requirements → technical design → operational ownership**

---

# 📊 Clickstream Analytics Platform

[`clickstream-analytics/`](clickstream-analytics/)

A high-volume, event-driven analytics architecture designed for web and product behavioral telemetry.

## Architecture

```text
Client
  ↓
API Gateway
  ↓
AWS WAF
  ↓
Ingestion Lambda
  ↓
Kinesis Data Streams
  ↓
Processing Lambda
  ├──────────────→ OpenSearch
  │
  ↓
Firehose
  ↓
S3 Parquet
  ↓
Glue
  ↓
Athena
```

## Modeled Capacity

```text
1,000 sustained events/sec
5,000 peak events/sec
86.4M events/day
~88.5 GB/day raw
~2.65 TB/month raw
```

## Architecture Topics

- Streaming ingestion
- Session ordering
- Schema validation
- Kinesis replay
- Lambda partial-batch failures
- DLQ / replay
- OpenSearch serving layer
- S3 durable system of record
- Parquet
- Athena optimization
- RTO / RPO
- Capacity planning
- FinOps

---

# 🛰️ IoT Sensor Analytics Platform

[`iot-sensor-analytics/`](iot-sensor-analytics/)

A secure industrial IoT telemetry architecture.

## Architecture

```text
Industrial Device
      ↓ MQTT / TLS
AWS IoT Core
      ↓
IoT Rules Engine
      ↓
Kinesis
      ↓
Lambda Anomaly Detection
   ├────────→ SNS Alerts
   ├────────→ OpenSearch
   │
   ↓
Firehose
   ↓
S3 Parquet
   ↓
Glue / Athena
   ↓
QuickSight
```

## Modeled Fleet

```text
10,000 devices
1 message/device/minute
14.4M messages/day
~166.7 sustained messages/sec
1,000 message/sec burst target
```

## Security

- X.509 device certificates
- Device-specific IoT policies
- Certificate rotation/revocation
- KMS
- IAM
- CloudTrail
- Private analytics services
- Strict telemetry schema

## Reliability

- Offline-device strategy
- Edge buffering
- Reconnect storms
- Duplicate/out-of-order events
- Kinesis backlog
- Poison messages
- Replay
- Regional DR

---

# 🏥 Healthcare Data Platform

[`healthcare-data-platform/`](healthcare-data-platform/)

A secure analytics architecture focused on regulated healthcare data.

> This is a simulated healthcare architecture demonstrating **HIPAA-aligned technical patterns**. It does not claim certification or legal compliance.

## Architecture

```text
Clinical / Operational Sources
            ↓
        Ingestion
            ↓
      S3 Landing Zone
            ↓
 Validation / De-identification
            ↓
      S3 Curated Parquet
            ↓
      Lake Formation
            ↓
     Glue Data Catalog
       ├───────────┐
       ↓           ↓
    Athena      Redshift
       └──────┬────┘
              ↓
          QuickSight
```

## Security / Governance

- PHI segregation
- Minimum-necessary access
- IAM federation
- Lake Formation
- KMS
- CloudTrail
- GuardDuty
- Security Hub
- Macie
- De-identification
- Audit controls
- Break-glass access pattern

## Recovery

```text
RTO: 4 hours
RPO: 15 minutes
```

---

# 🛒 Retail Analytics Platform

[`retail-analytics-platform/`](retail-analytics-platform/)

A multi-channel retail analytics architecture designed to replace next-day spreadsheet reporting with near-real-time business intelligence.

## Business Scenario

```text
320 stores
~4.2M transactions/day
Store POS + Ecommerce
<30-minute analytics freshness target
```

## Architecture

```text
POS / Ecommerce / Inventory
            ↓
      API Gateway
            ↓
         Lambda
            ↓
         Kinesis
            ↓
       S3 Landing
            ↓
          Glue
            ↓
      S3 Curated
       ├─────────────┐
       ↓             ↓
     Athena       Redshift
       └──────┬──────┘
              ↓
          QuickSight
```

## Analytics

- Net Sales
- Gross Margin
- AOV
- Return Rate
- Sell-Through
- Stockout Rate
- Inventory Turnover
- Promotion Lift
- Store Performance
- Channel Contribution

## Architecture Topics

- Streaming + batch
- Star schema
- Data quality
- Reconciliation
- Lake Formation
- DR
- FinOps
- Executive BI

---

# 💸 AWS FinOps Framework

[`finops/`](finops/)

A reusable cloud financial management framework demonstrating:

```text
Inform
  ↓
Allocate
  ↓
Detect
  ↓
Optimize
  ↓
Govern
  ↓
Measure
```

## Modeled Cost Baseline

```text
$54,000/month
```

Major modeled cost areas include:

- EC2 / ECS
- RDS / Aurora
- OpenSearch
- NAT / Data Transfer
- S3
- CloudWatch
- Backups
- Lambda / APIs

## FinOps Capabilities

- AWS Cost Explorer
- AWS Budgets
- Cost Anomaly Detection
- Tagging standards
- Cost allocation
- Forecasting
- Rightsizing
- Graviton
- Storage lifecycle
- Network optimization
- Savings Plans / RIs
- Unit economics
- Executive reporting
- Python automation

### Core Governance Targets

```text
Tagged Spend ≥ 98%
Unallocated Spend < 2%
Forecast Variance < 10%
```

Projected savings are intentionally kept separate from **realized savings**.

---

# 🧰 AWS Cloud Consulting Toolkit

[`consulting-toolkit/`](consulting-toolkit/)

A reusable AWS consulting framework covering the full customer lifecycle.

## Lifecycle

```text
Client Intake
      ↓
Discovery
      ↓
Assessment
      ↓
Target Architecture
      ↓
Architecture Decisions
      ↓
Delivery Planning
      ↓
FinOps
      ↓
Operational Handover
      ↓
Executive Closeout
```

## Included Artifacts

### Intake

- Client questionnaire
- Discovery workshop
- Stakeholder map

### Assessment

- AWS Well-Architected review
- Security assessment
- Cloud maturity scorecard

### Architecture

- High-level design
- Requirements traceability
- Threat model
- ADRs

### Delivery

- Project plan
- RAID log
- Weekly status reporting

### Financial

- FinOps playbook
- Savings model

### Presales

- Statement of Work
- LOE estimator
- Executive one-pager

### Handover

- Operations runbook
- Knowledge transfer
- Operational acceptance

### Example Engagement

A fully completed simulated modernization engagement demonstrates how all of the artifacts work together.

---

# 🏗️ Architecture Philosophy

Across the portfolio, architectures follow several consistent principles.

## Security by Default

```text
Federated Identity
      ↓
Least Privilege
      ↓
Private Data Tiers
      ↓
Encryption
      ↓
Audit Logging
      ↓
Threat Detection
```

---

## Reliability by Design

Architectures use combinations of:

- Multi-AZ
- Health checks
- Autoscaling
- Managed failover
- Durable event buffering
- Backups
- Replay
- Cross-region recovery
- Runbooks
- Failure-mode analysis

---

## Infrastructure as Code

Projects use:

- Terraform
- AWS CDK
- Python

Infrastructure changes are designed around:

```text
Source Control
      ↓
Pull Request
      ↓
Validation
      ↓
Security Scan
      ↓
Plan / Synth
      ↓
Review
      ↓
Controlled Deployment
```

---

# 🔐 Security Architecture

Security controls demonstrated throughout the portfolio include:

### Identity

- IAM
- IAM roles
- Federated access
- Short-lived credentials
- GitHub OIDC

### Encryption

- AWS KMS
- S3 encryption
- Database encryption
- TLS

### Detection

- CloudTrail
- AWS Config
- GuardDuty
- Security Hub
- CloudWatch

### Edge Protection

- AWS WAF
- API throttling
- Rate controls

### Data Governance

- Lake Formation
- S3 access controls
- Data classification
- De-identification
- Least-privilege analytics access

---

# 📡 Observability

Architectures include monitoring around the four primary signal categories:

```text
Latency
Traffic
Errors
Saturation
```

Common services:

- Amazon CloudWatch
- CloudWatch Logs
- CloudWatch Alarms
- Amazon SNS
- CloudTrail
- VPC Flow Logs

Example monitored conditions:

- HTTP 5xx
- Kinesis iterator age
- Lambda errors
- ECS capacity
- RDS CPU/connections
- OpenSearch cluster health
- Firehose failures
- Missing data feeds
- Silent IoT devices
- Cost anomalies

---

# 🔁 Disaster Recovery

Recovery planning is treated as an architecture requirement rather than a documentation afterthought.

Each major project defines:

```text
RTO
RPO
Recovery Strategy
Backup Strategy
Failure Modes
Recovery Procedure
Validation
```

Patterns include:

- Multi-AZ
- Point-in-time recovery
- S3 replication
- Cross-region backups
- IaC rebuild
- Data reconciliation
- Controlled failback

---

# 💰 FinOps Across the Portfolio

Cost is treated as part of architecture.

Projects include planning around:

- Rightsizing
- Autoscaling
- Storage lifecycle
- Parquet
- Partition pruning
- Graviton
- NAT reduction
- OpenSearch lifecycle
- CloudWatch retention
- Commitment planning
- Unit economics

The decision framework is:

```text
Observe
  ↓
Remove Waste
  ↓
Rightsize
  ↓
Optimize Architecture
  ↓
Measure
  ↓
Commit
```

---

# 📝 Architecture Decision Records

Major technical choices are documented using ADRs.

Examples include:

- ECS/Fargate vs alternatives
- Managed database selection
- Kinesis vs queue/broker alternatives
- Parquet partitioning
- OpenSearch serving layer
- Multi-AZ
- Regional DR
- Federated identity
- IaC standards
- Lake Formation
- Streaming vs batch

The goal is to demonstrate **tradeoff reasoning**, not just AWS service familiarity.

---

# 🧪 Validation & Evidence

The upgraded projects include evidence folders containing artifacts such as:

- Validation reports
- Acceptance criteria
- Artifact manifests
- SHA-256 hashes
- Architecture review records
- Reconciliation reports
- Simulated load/freshness reports
- Security-control maps
- Operational acceptance evidence
- Anomaly test cases

The portfolio clearly separates:

```text
Executed Evidence
vs
Modeled / Simulated Evidence
```

If a benchmark, cost reduction, or recovery exercise was not executed against a live AWS account, it is not presented as a production result.

---

# 🧠 AWS Well-Architected Alignment

The portfolio demonstrates thinking across all six pillars.

## Operational Excellence

- IaC
- CI/CD
- Runbooks
- SLOs
- Game days
- Operational ownership

## Security

- IAM
- Encryption
- Detection
- Threat modeling
- Governance

## Reliability

- Multi-AZ
- Event durability
- Backup/recovery
- RTO/RPO

## Performance Efficiency

- Managed services
- Autoscaling
- Capacity planning
- Query optimization

## Cost Optimization

- FinOps
- Rightsizing
- Storage lifecycle
- Commitments
- Unit economics

## Sustainability

- Elastic infrastructure
- Managed services
- Storage lifecycle
- Reduced idle capacity

---

# 🧰 Technologies & Tools

## AWS Compute

- AWS Lambda
- Amazon ECS
- AWS Fargate

## Networking

- Amazon VPC
- Application Load Balancer
- NAT Gateway
- VPC Endpoints
- Route 53
- CloudFront

## Data

- Amazon S3
- Amazon RDS
- Amazon Redshift Serverless
- AWS Glue
- Amazon Athena
- AWS Lake Formation

## Streaming

- Amazon Kinesis
- Amazon Data Firehose
- AWS IoT Core

## Analytics

- Amazon QuickSight
- Amazon OpenSearch Service

## Security

- AWS IAM
- AWS KMS
- AWS WAF
- AWS Secrets Manager
- CloudTrail
- AWS Config
- GuardDuty
- Security Hub
- Macie

## Operations

- Amazon CloudWatch
- Amazon SNS

## Automation

- Python
- Terraform
- AWS CDK
- GitHub Actions

---

# 🎓 Skills Demonstrated

**AWS Solutions Architecture • Cloud Consulting • AWS Professional Services • AWS Well-Architected Framework • Terraform • AWS CDK • Python • VPC • ECS/Fargate • Lambda • RDS • S3 • Kinesis • Firehose • IoT Core • Athena • Glue • Redshift • QuickSight • OpenSearch • IAM • KMS • WAF • GuardDuty • Security Hub • CloudTrail • CloudWatch • Lake Formation • FinOps • Disaster Recovery • RTO/RPO • Threat Modeling • Architecture Decision Records • Capacity Planning • Data Governance • Event-Driven Architecture • Customer Discovery • LOE Estimation • Operational Handoff**

---

# 💼 Portfolio Interview Story

A concise explanation of the entire repository:

> I built this AWS Solutions Architect portfolio to demonstrate more than individual AWS labs. Each project starts with a business problem and then works through requirements, architecture decisions, security, reliability, infrastructure automation, observability, cost, recovery, and validation. The portfolio includes customer-facing consulting artifacts as well as hands-on technical implementations using Terraform, AWS CDK, Python, Kinesis, Lambda, ECS/Fargate, RDS, S3, Athena, Glue, OpenSearch, IoT Core, and other AWS services. I also clearly separate modeled architecture assumptions from real production evidence so that the projects remain technically defensible.

---

# 🚀 Suggested Review Order

For recruiters or interviewers:

### 1. AWS Professional Services Portfolio

Shows the complete customer consulting lifecycle.

### 2. Clickstream Analytics

Shows streaming, event-driven, data-platform architecture.

### 3. IoT Sensor Analytics

Shows device security, MQTT, streaming, anomaly detection, and fleet reliability.

### 4. Healthcare Data Platform

Shows regulated-data architecture, governance, and security.

### 5. Retail Analytics Platform

Shows business intelligence, data architecture, and executive analytics.

### 6. FinOps Framework

Shows cost ownership and optimization.

### 7. Consulting Toolkit

Shows repeatable consulting methodology and customer delivery.

---

# 🏁 Final Takeaway

This repository demonstrates the complete AWS Solutions Architect mindset:

```text
Business Outcome
      ↓
Discovery
      ↓
Requirements
      ↓
Architecture
      ↓
Tradeoffs
      ↓
Security
      ↓
Automation
      ↓
Observability
      ↓
Reliability
      ↓
Disaster Recovery
      ↓
FinOps
      ↓
Validation
      ↓
Operational Ownership
```

The goal is not simply to demonstrate familiarity with AWS services.

The goal is to demonstrate the ability to design **secure, scalable, reliable, cost-aware AWS systems that connect technical decisions directly to business outcomes.**

---

## ⚠️ Portfolio Scope & Evidence Policy

This repository contains **simulated architecture engagements, reference implementations, modeled workloads, and portfolio scenarios**.

Unless specifically supported by deployment/test evidence:

- Modeled cost reductions are not represented as realized savings.
- Capacity targets are not represented as measured production throughput.
- RTO/RPO values are architecture objectives rather than claimed production achievements.
- Example customers are fictional.
- Healthcare controls are technical design patterns, not a compliance certification.
- Portfolio alignment with AWS certification subject areas does not imply certification status.

This policy keeps the repository **technically credible, transparent, and interview-defensible**.

---

## 👤 Author

**Jamie Christian II**

**Focus:** AWS Solutions Architecture • Cloud Consulting • Security • FinOps • Cloud Platforms

**GitHub:** [github.com/JamieChristian22](https://github.com/JamieChristian22)
