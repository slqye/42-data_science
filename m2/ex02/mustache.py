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


def debug_math(data) -> None:
	df = pd.DataFrame(data, columns=["price"])
	print(f"count\t{df.count()['price']}")
	print(f"mean\t{df.mean()['price']}")
	print(f"std\t{df.std()['price']}")
	print(f"min\t{df.min()['price']}")
	print(f"25%\t{df.quantile(0.25)['price']}")
	print(f"50%\t{df.quantile(0.5)['price']}")
	print(f"75%\t{df.quantile(0.75)['price']}")
	print(f"max\t{df.max()['price']}")


def first_chart(data) -> None:
	df = pd.DataFrame(data, columns=["price"])
	sns.boxplot(
		data=df,
		legend=False,
		orient="h",
		flierprops={
			"marker": "d",
			"markerfacecolor": "gray",
			"markeredgecolor": "gray"
		}
	)
	plt.yticks([])
	plt.xlabel("price")
	plt.ylabel("")
	plt.show()
	plt.close()


def second_chart(data) -> None:
	df = pd.DataFrame(data, columns=["price"])
	sns.boxplot(
		data=df,
		legend=False,
		orient="h",
		showfliers=False,
		color="lightgreen"
	)
	plt.yticks([])
	plt.xlabel("price")
	plt.ylabel("")
	plt.show()
	plt.close()


def third_chart(data) -> None:
	df = pd.DataFrame(data, columns=["date", "amount"])
	df["date"] = pd.to_datetime(df["date"])
	sns.boxplot(
		data=df,
		x="amount",
		legend=False,
		orient="h",
		flierprops={
			"marker": "d",
			"markerfacecolor": "gray",
			"markeredgecolor": "gray"
		}
	)
	plt.xlabel("")
	plt.ylabel("")
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
		debug_math(get_data(session, "mustache.1.sql"))
		first_chart(get_data(session, "mustache.2.sql"))
		second_chart(get_data(session, "mustache.3.sql"))
		third_chart(get_data(session, "mustache.4.sql"))
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()


if __name__ == "__main__":
	main()
