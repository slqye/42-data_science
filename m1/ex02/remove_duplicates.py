import sys
import psycopg2
import time


def join_tables(config: dict):
	start_time = time.time()
	name = "customers"
	cmd_remove_duplicates = (
		f"""
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
		DELETE FROM {name}
		WHERE ctid IN (SELECT ctid FROM duplicates);
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
