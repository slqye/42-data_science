import sys
import psycopg2


def create_table(config: dict, path: str):
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
			user_session UUID NOT NULL
		);
		"""
	)
	cmd_insert_data = (
		f"""
		INSERT INTO {name} (event_time, event_type, product_id, price, user_id, user_session)
		VALUES (%s, %s, %s, %s, %s, %s);
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
					user_session
				))
	try:
		with psycopg2.connect(config) as conn:
			with conn.cursor() as cursor:
				print(f"Creating table {name}...")
				cursor.execute(cmd_create_table)
				print(f"Table {name} created successfully.")
				print(f"Inserting data into {name}...")
				cursor.executemany(cmd_insert_data, table_data)
				print(f"Data inserted into {name} successfully.")
	except Exception as e:
		print(f"Error creating table {name}: {e}", file=sys.stderr)


def main(argv: list):
	config = {
		"host": "localhost",
		"port": "5432",
		"user": "uwywijas",
		"password": "mysecretpassword",
		"dbname": "piscineds"
	}
	for path in argv[1:]:
		if path.endswith(".csv"):
			print(f"[{path}]")
			create_table(config, path)
		else:
			print(f"[{path}]: not a CSV file.")


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: python3 table.py [path_to_csv_file]", file=sys.stderr)
		sys.exit(1)
	main(sys.argv)
