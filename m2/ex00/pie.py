import psycopg2
import matplotlib.pyplot as plt
import numpy as np


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


def main():
	with PostgreSqlConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT event_type FROM customers")
		data = cursor.fetchall()
	if not data:
		print("No data found.")
		return
	length = len(data)
	values = [
		data.count(("view",)) * 100 / length,
		data.count(("cart",)) * 100 / length,
		data.count(("remove_from_cart",)) * 100 / length,
		data.count(("purchase",)) * 100 / length
	]
	fig, ax = plt.subplots()
	ax.pie(
		values,
		labels=["view", "cart", "remove_from_cart", "purchase"],
		autopct="%1.1f%%"
	)
	fig.savefig("/mnt/c/Users/Slaye/Desktop/pie.png")


if __name__ == "__main__":
	main()
