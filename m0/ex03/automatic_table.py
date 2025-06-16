import sys
import os
import psycopg2
from psycopg2.extras import execute_values
import time


def create_table(config: dict, path: str):
	start_time = time.time()
	name = path.split("/")[-1].split(".")[0]
	table_data = []
	cmd_create_table = (
		f"""
		CREATE TABLE IF NOT EXISTS {name} (
			event_time TIMESTAMPTZ NOT NULL,
			event_type TEXT NOT NULL,
			product_id INTEGER NOT NULL,
			price NUMERIC(10, 2) NOT NULL,
			user_id BIGINT NOT NULL,
			user_session UUID
		);
		"""
	)
	cmd_insert_data = (
		f"""
		INSERT INTO {name} (event_time, event_type, product_id, price, user_id, user_session)
		VALUES %s;
		"""
	)
	with open(path, "r") as file:
		next(file)
		for line in file:
			parts = line.strip().split(",")
			if len(parts) == 6:
				event_time, event_type, product_id, price, user_id, user_session = parts
				table_data.append((
					event_time,
					event_type,
					int(product_id),
					float(price),
					int(user_id),
					user_session if user_session.strip() else None
				))
	try:
		with psycopg2.connect(**config) as conn:
			with conn.cursor() as cursor:
				cursor.execute(f"SELECT 1 FROM {name} LIMIT 1")
				if (cursor.fetchone() is not None):
					print(f"[{name}]: Table already exists, skipping")
					print(f"[{name}]: Done in {time.time() - start_time:.2f}s")
					return
				print(f"[{name}]: Creating table")
				cursor.execute(cmd_create_table)
				print(f"[{name}]: Table successfully created")
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
	path = "../../../subject/customer/"
	files = os.listdir(path)
	for file in files:
		if file.endswith(".csv"):
			create_table(config, os.path.join(path, file))


if __name__ == "__main__":
	main()
