-- data_catalog_tables.sql
-- Example Athena / Glue Catalog DDL for curated tables

CREATE EXTERNAL TABLE IF NOT EXISTS curated.fact_sales (
    timestamp_utc        timestamp,
    store_id             string,
    sku                  string,
    qty_sold             int,
    unit_price           double,
    gross_margin_est     double,
    on_hand_qty          int,
    reorder_point        int
)
PARTITIONED BY (
    date_key string,
    store_id_partition string
)
STORED AS PARQUET
LOCATION 's3://retail-analytics-platform/curated/fact_sales/';
