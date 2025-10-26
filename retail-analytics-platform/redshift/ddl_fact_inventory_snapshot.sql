CREATE TABLE fact_inventory_snapshot (
    snapshot_id     BIGINT IDENTITY(1,1),
    timestamp_utc   TIMESTAMP,
    store_id        VARCHAR(20),
    sku             VARCHAR(50),
    on_hand_qty     INTEGER,
    reorder_point   INTEGER,
    risk_flag       VARCHAR(20)
);
