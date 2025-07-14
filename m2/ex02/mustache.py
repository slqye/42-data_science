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
	plt.boxplot(
		[float(x[3]) for x in data],
		orientation="horizontal",
		patch_artist=True,
		flierprops=dict(
			marker="d",
			color="gray",
			markerfacecolor="gray",
			markeredgecolor="gray"
		),
		medianprops=dict(
			color="green"
		),
		boxprops=dict(
			color="gray",
			facecolor="gray"
		),
		whiskerprops=dict(
			color="gray"
		),
		capprops=dict(
			color="gray"
		),
		widths=2
	)
	plt.grid(axis="x")
	plt.xlabel("price")
	plt.yticks([])
	plt.show()


def second_chart(data: list):
	plt.boxplot(
		[float(x[3]) for x in data],
		orientation="horizontal",
		patch_artist=True,
		showfliers=False,
		medianprops=dict(
			color="black"
		),
		boxprops=dict(
			facecolor="lightgreen"
		),
		widths=2
	)
	plt.grid(axis="x")
	plt.xlabel("price")
	plt.yticks([])
	plt.show()


def third_chart(data: list):
	plt.boxplot(
		[round(float(x[1])) for x in data],
		orientation="horizontal",
		patch_artist=True,
		flierprops=dict(
			marker="d",
			color="gray",
			markerfacecolor="gray",
			markeredgecolor="gray"
		),
		medianprops=dict(
			color="black"
		),
		boxprops=dict(
			facecolor="lightblue"
		),
		widths=2,
		whis=0.2
	)
	plt.grid(axis="x")
	plt.yticks([])
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
	# print_math(data)
	# first_chart(data)
	# second_chart(data)
	with PostgreSqlConnection() as conn:
		cursor = conn.cursor()
		cursor.execute(
			"""
			SELECT user_id, AVG(price) AS mean_cart_price FROM customers
			WHERE event_type = 'cart'
			GROUP BY user_id
			HAVING AVG(price) BETWEEN 26 AND 43;
			"""
		)
		data = cursor.fetchall()
	if not data:
		print("No data found.")
		return
	third_chart(data)


if __name__ == "__main__":
	main()
