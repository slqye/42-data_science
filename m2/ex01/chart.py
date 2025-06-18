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


def first_chart(data: list):
	all_dates = [x[0].date() for x in data]
	dates = sorted(list(dict.fromkeys(all_dates)))
	customers = [all_dates.count(x) for x in dates]
	ticks = []
	for i in range(len(dates)):
		if i == 0:
			ticks.append(dates[i])
		elif dates[i - 1] not in ticks and dates[i].month != dates[i - 1].month:
			ticks.append(dates[i])
	plt.plot(dates, customers)
	plt.xticks(ticks, [x.strftime("%b") for x in ticks])
	plt.ylabel("Number of customers")
	plt.savefig("/mnt/c/Users/Slaye/Desktop/chart.png")


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
	first_chart(data)


if __name__ == "__main__":
	main()
