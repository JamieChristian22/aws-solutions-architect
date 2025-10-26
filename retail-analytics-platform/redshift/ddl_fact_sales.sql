CREATE TABLE fact_sales (
    sales_id            BIGINT IDENTITY(1,1),
    timestamp_utc       TIMESTAMP,
    date_key            VARCHAR(8),
    store_id            VARCHAR(20),
    sku                 VARCHAR(50),
    qty_sold            INTEGER,
    unit_price          DECIMAL(10,2),
    gross_margin_est    DECIMAL(10,2),
    on_hand_qty         INTEGER,
    reorder_point       INTEGER
);
