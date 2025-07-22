SELECT DATE(event_time), COUNT(event_time) FROM customers
WHERE event_type = 'purchase'
GROUP BY DATE(event_time);
