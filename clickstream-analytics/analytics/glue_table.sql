CREATE EXTERNAL TABLE IF NOT EXISTS clickstream_events (
  event_id string,
  event_time timestamp,
  session_id string,
  anonymous_id string,
  user_id string,
  event_type string,
  page_url string,
  referrer string,
  device_type string,
  source string,
  campaign string,
  revenue double,
  properties map<string,string>,
  processed_at timestamp
)
PARTITIONED BY (
  event_date string,
  event_hour string
)
STORED AS PARQUET
LOCATION 's3://processed-clickstream/events/'
TBLPROPERTIES ('parquet.compress'='SNAPPY');
