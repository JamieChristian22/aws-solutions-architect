SELECT device_id,
       date_trunc('hour', from_iso8601_timestamp(ts)) AS hour_bucket,
       avg(temp_c) AS avg_temp_c
FROM iot_telemetry.readings
WHERE from_iso8601_timestamp(ts) >= current_timestamp - INTERVAL '24' hour
GROUP BY 1,2
ORDER BY 2 DESC, 1 ASC;
