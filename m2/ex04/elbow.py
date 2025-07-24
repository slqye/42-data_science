import sqlalchemy as sqla
import sqlalchemy.orm as sqlaorm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_sql_file(path: str) -> str:
	data: str = ""
	with open(path, "r") as file:
		data = file.read().replace("\n", " ")
	return data


def users_chart(data) -> None:
	df = pd.DataFrame(data, columns=["purchases", "total_spent"])
	sns.relplot(
		data=df,
		x="purchases",
		y="total_spent",
		legend=False,
	)
	plt.xlabel("number of purchases")
	plt.ylabel("total spent")
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
		users_chart(get_data(session, "elbow.1.sql"))
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()


if __name__ == "__main__":
	main()
