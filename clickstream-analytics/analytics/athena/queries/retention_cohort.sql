WITH first_seen AS (
  SELECT user_id, date(min(from_iso8601_timestamp(created_at))) first_day FROM clickstream.events GROUP BY 1
), activity AS (
  SELECT user_id, date(from_iso8601_timestamp(created_at)) day FROM clickstream.events
)
SELECT fs.first_day cohort, date_diff('week', fs.first_day, a.day) wk, count(distinct a.user_id) users
FROM first_seen fs JOIN activity a USING(user_id)
WHERE wk BETWEEN 0 AND 4
GROUP BY 1,2 ORDER BY 1,2;