BEGIN;

ALTER TABLE customers
ADD COLUMN IF NOT EXISTS category_id BIGINT,
ADD COLUMN IF NOT EXISTS category_code TEXT,
ADD COLUMN IF NOT EXISTS brand TEXT;

WITH ranked_items AS (
    SELECT
        product_id,
        category_id,
        category_code,
        brand,
        ROW_NUMBER() OVER (
            PARTITION BY product_id
            ORDER BY 
                (CASE WHEN category_id IS NOT NULL THEN 1 ELSE 0 END +
                 CASE WHEN category_code IS NOT NULL THEN 1 ELSE 0 END +
                 CASE WHEN brand IS NOT NULL THEN 1 ELSE 0 END) DESC
        ) AS rn
    FROM items
),
best_items AS (
    SELECT *
    FROM ranked_items
    WHERE rn = 1
)

UPDATE customers
SET
    category_id = best_items.category_id,
    category_code = best_items.category_code,
    brand = best_items.brand
FROM best_items
WHERE best_items.product_id = customers.product_id;

COMMIT;
