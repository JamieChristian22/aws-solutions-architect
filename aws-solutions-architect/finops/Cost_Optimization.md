# Cost Optimization / FinOps

## Planning Baseline
This portfolio uses an explicit **architecture planning model**, not a claim about a live AWS bill. Actual AWS cost depends on region, usage, pricing changes, negotiated discounts, and workload behavior.

Modeled baseline: **$28,000/month**  
Modeled optimization backlog: **$5,790/month**  
Modeled optimized run rate: **$22,210/month**  
Modeled annual savings opportunity: **$69,480/year**  
Modeled reduction: **20.7%**

## Optimization Backlog
| Action | Monthly Savings Model |
|---|---:|
| Fargate rightsizing/autoscaling | $1,800 |
| Graviton-compatible workload migration | $900 |
| RDS rightsizing after observed utilization | $950 |
| S3/log lifecycle and retention tuning | $420 |
| NAT traffic reduction using VPC endpoints | $620 |
| Savings Plan after stable baseline | $1,100 |
| **Total** | **$5,790** |

## Governance
- Mandatory cost allocation tags.
- Monthly budget threshold review at 50%, 80%, and 100%.
- Weekly anomaly review during first 60 days after launch.
- Rightsizing review after 30 days of representative metrics.
- Commitment purchase only after usage stability and architecture approval.
- Nonproduction shutdown schedules considered for suitable workloads.

## Decision Rule
Do not trade away required RTO/RPO, security, or availability purely to reduce cost. Cost optimization is evaluated against business requirements.
