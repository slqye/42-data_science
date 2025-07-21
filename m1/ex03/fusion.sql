BEGIN;

ALTER TABLE customers
ADD COLUMN IF NOT EXISTS category_id BIGINT,
ADD COLUMN IF NOT EXISTS category_code TEXT,
ADD COLUMN IF NOT EXISTS brand TEXT;

UPDATE customers
SET
	category_id = items.category_id,
	category_code = items.category_code,
	brand = items.brand
FROM items
WHERE items.product_id = customers.product_id;

COMMIT;
