# Requirements Traceability

| ID | Requirement | Design Control | Validation |
|---|---|---|---|
| NFR-01 | 99.9% availability | Multi-AZ app/data | AZ game day |
| NFR-02 | RTO 60 min | DR runbook | recovery exercise |
| NFR-03 | RPO 15 min | PITR/backups | restore point review |
| SEC-01 | private DB | private subnet + SG | config check |
| SEC-02 | least privilege | scoped roles | IAM review |
| OPS-01 | monitored | alarms/SLOs | alarm test |
| FIN-01 | cost allocation | tags | tag compliance |
