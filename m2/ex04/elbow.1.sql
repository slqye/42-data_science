SELECT SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END), SUM(price) FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id;
