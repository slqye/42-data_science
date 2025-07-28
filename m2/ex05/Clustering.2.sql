SELECT
	ARRAY_AGG(DISTINCT event_time ORDER BY event_time),
	COUNT(*),
	SUM(price)
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id; 
