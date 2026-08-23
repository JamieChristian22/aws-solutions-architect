# Security Incident Response Playbook

## Phases
1. Detect and validate.
2. Classify severity.
3. Contain.
4. Preserve evidence.
5. Eradicate root cause.
6. Recover.
7. Conduct post-incident review.

## Credential Compromise
- revoke active sessions where practical
- disable affected access path
- inspect CloudTrail for anomalous actions
- rotate related secrets
- review permission changes and persistence mechanisms
- restore altered resources from known-good configuration

## Public Data Exposure
- block public access immediately
- preserve bucket/access/audit logs
- determine exposed object scope and timeframe
- rotate credentials/tokens present in affected data
- execute notification/legal process according to customer policy
- add preventive Config/Security Hub controls

## Evidence
Store incident timeline, finding IDs, CloudTrail event IDs, affected resource ARNs, actions taken, and recovery validation.
