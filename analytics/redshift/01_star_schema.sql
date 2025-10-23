-- analytics/redshift/01_star_schema.sql
-- Example star schema for purchases
CREATE TABLE IF NOT EXISTS dim_date (
  date_key INT PRIMARY KEY,
  dt DATE,
  year INT,
  month INT,
  day INT
);

CREATE TABLE IF NOT EXISTS dim_product (
  product_key INT IDENTITY(1,1) PRIMARY KEY,
  sku VARCHAR(50),
  category VARCHAR(100),
  price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS fact_sales (
  sales_key BIGINT IDENTITY(1,1) PRIMARY KEY,
  date_key INT REFERENCES dim_date(date_key),
  product_key INT REFERENCES dim_product(product_key),
  user_id VARCHAR(64),
  session_id VARCHAR(64),
  quantity INT,
  amount NUMERIC(12,2)
);
