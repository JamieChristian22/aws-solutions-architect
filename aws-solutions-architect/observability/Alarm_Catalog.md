# Alarm Catalog

| Alarm | Threshold | Severity | Action |
|---|---|---|---|
| ALB unhealthy hosts | >0 for 5 min | SEV-2 | inspect ECS/targets |
| ALB 5xx | >2% for 5 min | SEV-2 | inspect deployment/app logs |
| ECS running tasks | < desired for 10 min | SEV-2 | inspect task failures |
| ECS CPU | >80% for 15 min | SEV-3 | verify autoscaling/capacity |
| RDS CPU | >80% for 15 min | SEV-2 | Performance Insights |
| RDS free storage | <20% | SEV-2 | storage growth action |
| RDS connections | >80% of safe pool | SEV-2 | app pool/query review |
| GuardDuty high finding | any | SEV-1/2 | security playbook |
| AWS Budget 80% | monthly forecast/actual | FIN | finance/service owner review |
