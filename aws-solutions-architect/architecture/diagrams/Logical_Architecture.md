# Logical Architecture

```mermaid
flowchart LR
  Client --> DNS[Route 53]
  DNS --> CDN[CloudFront]
  CDN --> WAF[WAF]
  WAF --> LB[ALB]
  LB --> APP[ECS Fargate Service]
  APP --> DB[(RDS PostgreSQL Multi-AZ)]
  APP --> OBJ[(S3 Application Assets)]
  APP --> SM[Secrets Manager]
  APP --> CW[CloudWatch Logs/Metrics]
  CT[CloudTrail] --> LOG[(Audit Log Bucket)]
  CFG[AWS Config] --> SH[Security Hub]
  GD[GuardDuty] --> SH
  SH --> SNS[SNS / Incident Channel]
```

## Trust Boundaries
1. Internet to AWS edge.
2. Edge to public ALB.
3. ALB to private application tasks.
4. Application to private database.
5. Workload plane to security/observability services.
