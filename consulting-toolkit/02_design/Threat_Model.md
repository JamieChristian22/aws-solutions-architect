# Threat Model

Assets: customer data, secrets, AWS control plane, Terraform state, logs.

Threats:
- stolen credentials
- public data exposure
- privilege escalation
- destructive admin actions
- application injection
- supply-chain compromise
- ransomware
- data exfiltration

Controls:
federation/MFA, least privilege, KMS, WAF, private data tiers, CloudTrail, Config, GuardDuty, Security Hub, immutable/versioned backups, CI security scanning.
