SELECT
    patient_id,
    discharge_timestamp,
    first_outreach_timestamp,
    TIMESTAMPDIFF('hour', discharge_timestamp, first_outreach_timestamp) AS hours_to_first_outreach,
    CASE
        WHEN TIMESTAMPDIFF('hour', discharge_timestamp, first_outreach_timestamp) <= 48
        THEN 'ON TIME'
        ELSE 'LATE'
    END AS outreach_sla_status
FROM discharge_followup
ORDER BY discharge_timestamp DESC;