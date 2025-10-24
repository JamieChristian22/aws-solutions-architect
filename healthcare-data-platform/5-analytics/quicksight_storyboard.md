# QuickSight Dashboard Storyboard (Mocked Data)

## 1. High-Risk Patients Requiring Outreach Today
- Table of patients with `risk_score >= 80`
- Columns: patient_id, risk_score, last_outreach_status, last_outreach_ts
- Used internally by care coordinators

## 2. 30-Day Readmission Rate by Facility
- Bar or line chart
- Metric: % readmitted within 30 days (monthly trend)
- Audience: clinical leadership

## 3. Outreach SLA Compliance
- KPI tile: "% of discharges reached within 48 hours"
- Audience: quality / compliance

Row-level security:
- Care coordinators see only their assigned facility
- Executives see aggregate metrics (PHI minimized / partially de-identified)