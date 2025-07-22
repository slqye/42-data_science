SELECT date_trunc('month', event_time) as month, SUM(price) / 1000000 FROM customers
WHERE event_type = 'purchase'
GROUP BY month;
