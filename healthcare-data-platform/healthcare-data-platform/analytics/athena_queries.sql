SELECT facility_id, AVG(length_of_stay_days) avg_los
FROM curated_encounters
WHERE event_date BETWEEN DATE '2026-07-01' AND DATE '2026-07-31'
GROUP BY facility_id;

SELECT facility_id, COUNT(*) encounters
FROM curated_encounters
GROUP BY facility_id
ORDER BY encounters DESC;
