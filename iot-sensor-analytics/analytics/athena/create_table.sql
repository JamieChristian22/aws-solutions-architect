CREATE DATABASE IF NOT EXISTS iot_telemetry;

CREATE EXTERNAL TABLE IF NOT EXISTS iot_telemetry.readings (
  device_id        string,
  ts               string,
  ingested_at      string,
  temp_c           double,
  humidity_pct     double,
  vibration_g      double,
  battery_pct      double,
  anomalies        array<string>
)
PARTITIONED BY (
  year string,
  month string,
  day string,
  hour string
)
STORED AS PARQUET
LOCATION 's3://REPLACE_WITH_TELEMETRY_BUCKET/'
TBLPROPERTIES ('parquet.compression'='GZIP');
