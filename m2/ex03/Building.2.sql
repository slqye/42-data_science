SELECT
	SUM(CASE WHEN total >= -25 AND total < 25 THEN 1 ELSE 0 END),
	SUM(CASE WHEN total >= 25 AND total < 75 THEN 1 ELSE 0 END),
	SUM(CASE WHEN total >= 75 AND total < 125 THEN 1 ELSE 0 END),
	SUM(CASE WHEN total >= 125 AND total < 175 THEN 1 ELSE 0 END),
	SUM(CASE WHEN total >= 175 AND total < 225 THEN 1 ELSE 0 END)
FROM (
	SELECT user_id, SUM(price) AS total
	FROM customers
	WHERE event_type = 'purchase'
	GROUP BY user_id
) AS user_totals;
