CREATE TABLE dim_calendar (
    date_key        VARCHAR(8) PRIMARY KEY,
    timestamp_utc   TIMESTAMP,
    day_of_week     VARCHAR(10),
    week_num        INTEGER,
    fiscal_period   VARCHAR(20)
);
