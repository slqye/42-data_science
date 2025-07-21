import sys
import psycopg2
import time


def fusion(config: dict):
	start_time = time.time()
	name = "customers"
	cmd_add_columns = (
		f"""
		ALTER TABLE {name}
		ADD COLUMN IF NOT EXISTS category_id BIGINT,
		ADD COLUMN IF NOT EXISTS category_code TEXT,
		ADD COLUMN IF NOT EXISTS brand TEXT
		"""
	)
	cmd_join_tables = (
		f"""
		UPDATE {name} d
SET
	category_id = i.category_id,
	category_code = i.category_code,
	brand = i.brand
FROM (
	SELECT DISTINCT ON (product_id)
		product_id,
		category_id,
		category_code,
		brand
	FROM (
		SELECT *,
			(CASE WHEN category_id IS NULL THEN 1 ELSE 0 END +
			 CASE WHEN category_code IS NULL THEN 1 ELSE 0 END +
			 CASE WHEN brand IS NULL THEN 1 ELSE 0 END) AS null_count
		FROM items
	) sub
	ORDER BY product_id, null_count
) i
WHERE d.product_id = i.product_id;
		"""
	)

	try:
		with psycopg2.connect(**config) as conn:
			with conn.cursor() as cursor:
				print(f"[{name}]: Adding columns")
				cursor.execute(cmd_add_columns)
				print(f"[{name}]: Columns added successfully")
				print(f"[{name}]: Joining tables")
				cursor.execute(cmd_join_tables)
				print(f"[{name}]: 'Joined' successfully")
	except Exception as e:
		print(f"Error creating table [{name}]: {e}", file=sys.stderr)
	print(f"[{name}]: Done in {time.time() - start_time:.2f}s")


def main():
	config = {
		"host": "localhost",
		"port": "5432",
		"user": "uwywijas",
		"password": "mysecretpassword",
		"dbname": "piscineds"
	}
	fusion(config)


if __name__ == "__main__":
	main()
