SELECT event_type, COUNT(event_type) FROM customers
GROUP BY event_type;
