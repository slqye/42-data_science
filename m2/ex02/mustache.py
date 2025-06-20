import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


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


def print_math(data: list):
	print("count\t", len(data))
	print("mean\t", round(np.mean([d[3] for d in data]), 2))
	print("std\t", round(np.std([d[3] for d in data]), 2))
	print("min\t", np.min([d[3] for d in data]))
	print("25%\t", np.percentile([float(d[3]) for d in data], 25))
	print("55%\t", np.percentile([float(d[3]) for d in data], 50))
	print("75%\t", np.percentile([float(d[3]) for d in data], 75))
	print("max\t", np.max([d[3] for d in data]))


def first_chart(data: list):
	fig, ax = plt.subplots()
	ax.boxplot(
		x=[float(x[3]) for x in data],
		vert=False,
		flierprops=dict(marker='D')
	)
	ax.xaxis.grid(True)
	ax.set_xlabel('price')
	plt.show()


def main():
	with PostgreSqlConnection() as conn:
		cursor = conn.cursor()
		cursor.execute(
			"""
			SELECT * FROM customers
			WHERE event_type = 'purchase'
			"""
		)
		data = cursor.fetchall()
	if not data:
		print("No data found.")
		return
	print_math(data)
	first_chart(data)


if __name__ == "__main__":
	main()
