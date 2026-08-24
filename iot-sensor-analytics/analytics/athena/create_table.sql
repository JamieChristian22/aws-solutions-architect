CREATE EXTERNAL TABLE IF NOT EXISTS iot_telemetry (
 device_id string, site_id string, event_time timestamp, sequence_number bigint,
 temperature_c double, humidity_pct double, vibration_mm_s double, battery_pct double,
 firmware_version string, pressure_kpa double, motor_rpm bigint, anomalies array<string>
)
PARTITIONED BY (event_date string,event_hour string)
STORED AS PARQUET
LOCATION 's3://iot-telemetry-curated/telemetry/';
