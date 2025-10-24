CREATE DATABASE IF NOT EXISTS clickstream;
CREATE EXTERNAL TABLE IF NOT EXISTS clickstream.events (
  event_name string, user_id string, created_at string, received_at string, user_agent string, origin string, element_clicked string, time_spent int, source_menu string, page_url string
)
PARTITIONED BY (year string, month string, day string, hour string)
STORED AS PARQUET LOCATION 's3://REPLACE_PROCESSED_BUCKET/'
TBLPROPERTIES ('parquet.compression'='GZIP');