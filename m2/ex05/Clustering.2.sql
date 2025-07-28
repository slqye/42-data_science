SELECT
	COUNT(*) / COUNT(DISTINCT EXTRACT(MONTH FROM (event_time))),
	COUNT(*)
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id; 
