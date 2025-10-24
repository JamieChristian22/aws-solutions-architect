WITH steps AS (
  SELECT user_id,
    max(CASE WHEN event_name='page_view' THEN 1 ELSE 0 END) s1,
    max(CASE WHEN event_name='add_to_cart' THEN 1 ELSE 0 END) s2,
    max(CASE WHEN event_name='checkout' THEN 1 ELSE 0 END) s3
  FROM clickstream.events
  WHERE from_iso8601_timestamp(created_at) >= current_timestamp - INTERVAL '7' day
  GROUP BY user_id
)
SELECT sum(s1) step1, sum(CASE WHEN s1=1 AND s2=1 THEN 1 ELSE 0 END) step2,
       sum(CASE WHEN s1=1 AND s2=1 AND s3=1 THEN 1 ELSE 0 END) step3
FROM steps;