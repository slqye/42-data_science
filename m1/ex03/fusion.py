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
		UPDATE {name}
		SET
			category_id = items.category_id,
			category_code = items.category_code,
			brand = items.brand
		FROM items WHERE items.product_id = {name}.product_id
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
