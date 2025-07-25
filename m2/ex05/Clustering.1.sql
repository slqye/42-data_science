SELECT
	COUNT(*) / COUNT(DISTINCT TO_CHAR(event_time, 'YYYY-MM')),
	ARRAY_AGG(event_time ORDER BY event_time),
	SUM(price)
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id; 
