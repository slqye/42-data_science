import sys
import psycopg2
import time


def join_tables(config: dict):
	start_time = time.time()
	name = "customers"
	tables_names = []
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
	cmd_get_tables_names = (
		"""
		SELECT table_name
		FROM information_schema.tables
		WHERE table_schema = 'public'
			AND table_name LIKE 'data_%';
		"""
	)

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
				print(f"[{name}]: Retrieving existing tables")
				cursor.execute(cmd_get_tables_names)
				tables_names = cursor.fetchall()
				print(f"[{name}]: Found {len(tables_names)} tables to join")
				print(f"[{name}]: Joining data into table")
				for table in tables_names:
					table_name = table[0]
					cursor.execute(f"INSERT INTO {name} SELECT * FROM {table_name}")
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
	join_tables(config)


if __name__ == "__main__":
	main()
