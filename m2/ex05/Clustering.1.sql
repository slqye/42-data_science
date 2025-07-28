SELECT DISTINCT
	CASE
		WHEN monthly_purchases >= 5 THEN 'Loyal customers'
		WHEN monthly_purchases >= 2  THEN 'New customers'
		WHEN monthly_purchases >= 0 THEN 'inactive'
	END AS customer_segment,
	COUNT(DISTINCT user_id) AS customer_count
FROM (
	SELECT
		user_id,
		COUNT(*) / COUNT(DISTINCT TO_CHAR(event_time, 'YYYY-MM')) AS monthly_purchases,
		ARRAY_AGG(event_time ORDER BY event_time) AS purchase_dates,
		SUM(price) AS total_spent
	FROM customers
	WHERE event_type = 'purchase'
	GROUP BY user_id
) AS monthly_purchases
GROUP BY customer_segment
ORDER BY customer_count DESC;
