import sys
import psycopg2
import time


def join_tables(config: dict):
	start_time = time.time()
	name = "customers"
	cmd_remove_duplicates = (
		"""
		DELETE FROM SleepLogs log1
		using SleepLogs log2
		where log2.Id = log1.Id
			and log2.SleepDay = log1.SleepDay
			and log2.TotalMinutesAsleep = log1.TotalMinutesAsleep
			and log2.TotalTimeInBed = log1.TotalTimeInBed
			and log2.ctid < log1.ctid;
		"""
	)

	try:
		with psycopg2.connect(**config) as conn:
			with conn.cursor() as cursor:
				print(f"[{name}]: Joining data into table")
				cursor.execute(cmd_remove_duplicates)
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
