CREATE OR REPLACE VIEW curated_patient_risk AS
SELECT
    patient_id,
    risk_score,
    high_risk_flag,
    last_outreach_status,
    last_outreach_ts
FROM s3object
-- In production this would reference the Glue Catalog table for patient_risk parquet
;