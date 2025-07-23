SELECT user_id, COUNT(user_session) FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id
