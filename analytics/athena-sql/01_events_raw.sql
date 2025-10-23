-- analytics/athena-sql/01_events_raw.sql
CREATE EXTERNAL TABLE IF NOT EXISTS retail_analytics.events_raw (
  event string,
  user_id string,
  session_id string,
  sku string,
  price double,
  ts string
)
PARTITIONED BY (`year` string, `month` string, `day` string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://YOUR-LAKE-BUCKET/raw/ingest/'
TBLPROPERTIES ('projection.enabled'='true'); -- adjust after crawler creates schema
