import sqlalchemy as sqla
import sqlalchemy.orm as sqlaorm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def read_sql_file(path: str) -> str:
	data: str = ""
	with open(path, "r") as file:
		data = file.read().replace("\n", " ")
	return data


def first_chart(data) -> None:
	df = pd.DataFrame(data, columns=["user_id", "orders"])
	bins = np.linspace(0, 40, 6)
	sns.histplot(
		data=df,
		x="orders",
		bins=bins,
		legend=False,
	)
	plt.xticks(range(0, 39, 10))
	plt.xlabel("frequency")
	plt.ylabel("customers")
	plt.show()
	plt.close()


def second_chart(data) -> None:
	sns.barplot(
		x=[0, 50, 100, 150, 200],
		y=data[0],
		legend=False
	)
	plt.xlabel("monetary value in A")
	plt.ylabel("customers")
	plt.show()
	plt.close()


def get_data(session, sql_file: str) -> list:
	query = read_sql_file(sql_file)
	result = session.execute(sqla.text(query))
	data = result.fetchall()
	return data


def main():
	try:
		database = "postgresql://uwywijas:mysecretpassword@localhost:5432/piscineds"
		engine = sqla.create_engine(database)
		session = sqlaorm.sessionmaker(bind=engine)()
		sns.set_theme()
		first_chart(get_data(session, "Building.1.sql"))
		second_chart(get_data(session, "Building.2.sql"))
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()


if __name__ == "__main__":
	main()
