SELECT DATE(event_time), AVG(price) FROM customers
WHERE event_type = 'purchase'
GROUP BY DATE(event_time);
