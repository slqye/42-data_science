import sys
import psycopg2
import time


def join_tables(config: dict):
	start_time = time.time()
	name = "customers"
	cmd_remove_duplicates = (
		f"""
		CREATE TEMPORARY TABLE temp_customers AS SELECT DISTINCT * FROM customers;
		TRUNCATE customers;
		INSERT INTO {name} SELECT * FROM temp_customers;
		"""
	)

	try:
		with psycopg2.connect(**config) as conn:
			with conn.cursor() as cursor:
				print(f"[{name}]: Removing duplicates from table")
				cursor.execute(cmd_remove_duplicates)
				print(f"[{name}]: Removed {cursor.rowcount} duplicates successfully")
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
