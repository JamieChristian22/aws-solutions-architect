SELECT device_id,
       min(battery_pct) AS min_battery_pct,
       avg(battery_pct) AS avg_battery_pct
FROM iot_telemetry.readings
WHERE from_iso8601_timestamp(ts) >= current_timestamp - INTERVAL '24' hour
GROUP BY 1
ORDER BY min_battery_pct ASC;
