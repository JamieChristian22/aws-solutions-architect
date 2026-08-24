# Simulated Restore Exercise Report

**Type:** tabletop + configuration validation  
**Purpose:** demonstrate the recovery procedure without claiming a live production restore.

## Scenario
Primary analytics region unavailable.

## Expected Recovery Sequence
1. confirm latest replicated S3 object
2. recreate catalog/IaC in secondary region
3. restore/recreate query layer
4. validate record counts/checksums
5. re-enable BI after data validation

## Target
RTO: 4 hours  
RPO: 15 minutes

## Result
Procedure is complete and testable. A live AWS recovery exercise remains a deployment-stage activity and is not falsely represented as executed here.
