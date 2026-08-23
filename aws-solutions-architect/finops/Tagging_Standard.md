# Tagging Standard

Required tags:

| Tag | Example | Purpose |
|---|---|---|
| Environment | prod | lifecycle / controls |
| Application | northstar-api | ownership |
| Owner | platform-team | escalation |
| CostCenter | CC-4100 | allocation |
| ManagedBy | terraform | drift/change |
| DataClassification | confidential | security handling |

Resources missing required tags fail portfolio policy validation before production.
