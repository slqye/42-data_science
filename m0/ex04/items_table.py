import sys
import psycopg2
from psycopg2.extras import execute_values
import time


def create_table(config: dict, path: str):
	start_time = time.time()
	name = "items"
	table_data = []
	cmd_create_table = (
		f"""
		CREATE TABLE IF NOT EXISTS {name} (
			product_id INTEGER NOT NULL,
			category_id BIGINT,
			category_code TEXT,
			brand TEXT
		);
		"""
	)
	cmd_insert_data = (
		f"""
		INSERT INTO {name} (product_id, category_id, category_code, brand)
		VALUES %s;
		"""
	)
	with open(path, "r") as file:
		next(file)
		for line in file:
			parts = line.strip().split(",")
			if len(parts) == 4:
				product_id, category_id, category_code, brand = parts
				table_data.append((
					int(product_id),
					int(category_id) if category_id.isdigit() else None,
					category_code,
					brand
				))
	try:
		with psycopg2.connect(**config) as conn:
			with conn.cursor() as cursor:
				print(f"[{name}]: Creating table")
				cursor.execute(cmd_create_table)
				print(f"[{name}]: Table successfully created")
				cursor.execute(f"SELECT 1 FROM {name} LIMIT 1")
				if (cursor.fetchone() is not None):
					print(f"[{name}]: Table already exists, skipping")
					print(f"[{name}]: Done in {time.time() - start_time:.2f}s")
					return
				print(f"[{name}]: Inserting data into table")
				execute_values(cursor, cmd_insert_data, table_data)
				print(f"[{name}]: Data insertion completed")
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
	create_table(config, "../../../subject/item/item.csv")


if __name__ == "__main__":
	main()
