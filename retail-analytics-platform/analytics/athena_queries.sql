SELECT channel, SUM(net_sales) sales, SUM(gross_margin) margin
FROM fact_sales
WHERE event_date BETWEEN DATE '2026-08-01' AND DATE '2026-08-31'
GROUP BY channel;

SELECT store_id, SUM(stockout_flag) stockout_sku_days
FROM fact_inventory
GROUP BY store_id
ORDER BY stockout_sku_days DESC;
