# Data Governance Acceptance Test

## Test Cases
1. Analyst role cannot access restricted PHI landing zone.
2. Curated analytics dataset contains patient token instead of direct identifier.
3. Unknown sensitive/free-text field routes to quarantine.
4. Audit events record data-plane/control-plane changes.
5. Curated dataset schema matches published dictionary.
6. Data-quality failure blocks downstream executive refresh.

## Pass Criteria
All six controls must pass before the general analytics workspace is approved.
