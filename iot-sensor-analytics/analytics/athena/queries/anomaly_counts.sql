SELECT date_trunc('hour', from_iso8601_timestamp(ts)) AS hour_bucket,
       cardinality(anomalies) AS anomaly_count,
       anomalies
FROM iot_telemetry.readings
WHERE from_iso8601_timestamp(ts) >= current_timestamp - INTERVAL '24' hour
ORDER BY hour_bucket DESC;
