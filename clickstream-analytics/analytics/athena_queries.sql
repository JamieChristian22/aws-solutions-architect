-- Daily event volume
SELECT event_date, event_type, COUNT(*) events
FROM clickstream_events
WHERE event_date BETWEEN '2026-08-01' AND '2026-08-31'
GROUP BY event_date, event_type
ORDER BY event_date, events DESC;

-- Funnel by session
WITH s AS (
  SELECT session_id,
    MAX(CASE WHEN event_type='product_view' THEN 1 ELSE 0 END) product_view,
    MAX(CASE WHEN event_type='add_to_cart' THEN 1 ELSE 0 END) add_to_cart,
    MAX(CASE WHEN event_type='checkout_start' THEN 1 ELSE 0 END) checkout_start,
    MAX(CASE WHEN event_type='purchase' THEN 1 ELSE 0 END) purchase
  FROM clickstream_events
  WHERE event_date BETWEEN '2026-08-01' AND '2026-08-31'
  GROUP BY session_id
)
SELECT
  SUM(product_view) product_view_sessions,
  SUM(add_to_cart) cart_sessions,
  SUM(checkout_start) checkout_sessions,
  SUM(purchase) purchase_sessions
FROM s;

-- Revenue by acquisition source
SELECT source,
       COUNT(DISTINCT session_id) sessions,
       SUM(CASE WHEN event_type='purchase' THEN COALESCE(revenue,0) ELSE 0 END) revenue,
       SUM(CASE WHEN event_type='purchase' THEN 1 ELSE 0 END) purchases
FROM clickstream_events
WHERE event_date BETWEEN '2026-08-01' AND '2026-08-31'
GROUP BY source
ORDER BY revenue DESC;

-- Device conversion
SELECT device_type,
       COUNT(DISTINCT session_id) sessions,
       COUNT(DISTINCT CASE WHEN event_type='purchase' THEN session_id END) purchasing_sessions,
       COUNT(DISTINCT CASE WHEN event_type='purchase' THEN session_id END) * 1.0
         / NULLIF(COUNT(DISTINCT session_id),0) conversion_rate
FROM clickstream_events
WHERE event_date BETWEEN '2026-08-01' AND '2026-08-31'
GROUP BY device_type;
