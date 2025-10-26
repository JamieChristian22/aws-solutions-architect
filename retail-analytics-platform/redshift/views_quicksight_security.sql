-- Row-level security style view: store managers only see their region
CREATE OR REPLACE VIEW vw_sales_secure AS
SELECT fs.*
FROM fact_sales fs
JOIN dim_store ds ON fs.store_id = ds.store_id
WHERE ds.region = current_setting('app.user_region');
