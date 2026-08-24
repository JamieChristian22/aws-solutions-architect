# AWS Well-Architected Assessment

## Operational Excellence — 3/5
Strengths: Git-based source, basic monitoring.  
Gaps: manual infrastructure changes, incomplete runbooks.  
Actions: IaC, CI gates, operations runbook, game days.

## Security — 3/5
Strengths: MFA and encrypted storage.  
Gaps: inconsistent IAM scoping, incomplete centralized findings.  
Actions: federation, least privilege, Security Hub, GuardDuty, Config, threat model.

## Reliability — 2/5
Strengths: backups exist.  
Gaps: single-AZ dependencies and untested recovery.  
Actions: Multi-AZ, explicit RTO/RPO, restore testing, failure-mode review.

## Performance Efficiency — 3/5
Strengths: managed services.  
Gaps: no capacity baseline.  
Actions: load model, autoscaling, database performance review.

## Cost Optimization — 2/5
Strengths: cost owner exists.  
Gaps: weak tags and no recurring rightsizing review.  
Actions: tagging policy, budgets, anomaly detection, monthly FinOps cadence.

## Sustainability — 3/5
Strengths: managed/serverless adoption.  
Actions: autoscaling, storage lifecycle, idle-resource cleanup.
