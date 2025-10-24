SELECT
    facility_id,
    COUNT(DISTINCT CASE WHEN readmitted_within_30d = true THEN encounter_id END)
        * 100.0
        / NULLIF(COUNT(DISTINCT encounter_id),0) AS readmission_rate_pct,
    date_trunc('month', discharge_timestamp) AS month_bucket
FROM encounters_curated
GROUP BY facility_id, date_trunc('month', discharge_timestamp)
ORDER BY month_bucket DESC;