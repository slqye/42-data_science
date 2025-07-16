import psycopg2
import matplotlib.pyplot as plt


class PostgreSqlConnection:
	DB_HOST = "localhost"
	DB_PORT = "5432"
	DB_NAME = "piscineds"
	DB_USER = "uwywijas"
	DB_PASSWORD = "mysecretpassword"

	def __init__(self):
		self.conn = None

	def __enter__(self):
		self.conn = psycopg2.connect(
			host=self.DB_HOST,
			port=self.DB_PORT,
			dbname=self.DB_NAME,
			user=self.DB_USER,
			password=self.DB_PASSWORD
		)
		return self.conn

	def __exit__(self, exc_type, exc_value, traceback):
		if self.conn:
			self.conn.close()


def first_chart(data):
	users = {}
	for i in data:
		if i[0] not in users:
			users[i[0]] = 1
		else:
			users[i[0]] += 1
	plt.hist(users.values(), bins=5, zorder=2.0)
	plt.xlabel('frequency')
	plt.ylabel('customers')
	plt.grid()
	plt.show()


def second_chart(data):
	labels = ['0', '50', '100', '150', '200']
	y = [float(i) for i in data[0]]
	x = list(range(len(y)))
	plt.bar(x, y, zorder=2.0)
	plt.xlabel('monetary value in altarian dollars')
	plt.ylabel('customers')
	plt.xticks(x, labels)
	plt.grid()
	plt.show()


def main():
	with PostgreSqlConnection() as conn:
		cursor = conn.cursor()
		cursor.execute(
			"""
			SELECT
				SUM(CASE WHEN total >= 0 AND total < 50 THEN 1 ELSE 0 END),
				SUM(CASE WHEN total >= 50 AND total < 100 THEN 1 ELSE 0 END),
				SUM(CASE WHEN total >= 100 AND total < 150 THEN 1 ELSE 0 END),
				SUM(CASE WHEN total >= 150 AND total < 200 THEN 1 ELSE 0 END),
				SUM(CASE WHEN total >= 200 THEN 1 ELSE 0 END)
			FROM (
				SELECT user_id, SUM(price) AS total
				FROM customers
				WHERE event_type = 'purchase'
				GROUP BY user_id
			) AS user_totals;
			"""
		)
		data = cursor.fetchall()
	if not data:
		print("No data found.")
		return
	# first_chart(data)
	second_chart(data)


if __name__ == "__main__":
	main()
