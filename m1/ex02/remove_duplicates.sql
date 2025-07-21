WITH duplicates AS (
	SELECT a.ctid
	FROM customers a
	JOIN customers b
		ON a.ctid > b.ctid
		AND a.event_type = b.event_type
		AND a.product_id = b.product_id
		AND a.price = b.price
		AND a.user_id = b.user_id
		AND a.user_session = b.user_session
		AND ABS(EXTRACT(EPOCH FROM a.event_time - b.event_time)) <= 1
)
DELETE FROM customers
WHERE ctid IN (SELECT ctid FROM duplicates);
