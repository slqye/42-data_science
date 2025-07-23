SELECT DATE(event_time), SUM(price) / COUNT(DISTINCT user_id) FROM customers
WHERE event_type = 'purchase'
GROUP BY DATE(event_time)
