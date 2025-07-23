import sqlalchemy as sqla
import sqlalchemy.orm as sqlaorm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar


def read_sql_file(path: str) -> str:
	data: str = ""
	with open(path, "r") as file:
		data = file.read().replace("\n", " ")
	return data


def first_chart(data) -> None:
	df = pd.DataFrame(data, columns=["date", "count"])
	df["date"] = pd.to_datetime(df["date"])
	g = sns.lineplot(
		data=df,
		x="date",
		y="count",
		legend=False
	)
	monthly_ticks = df.groupby([df["date"].dt.year, df["date"].dt.month])["date"].min().sort_values()
	ticks = monthly_ticks.to_list()
	labels = [d.strftime("%b") for d in ticks]
	g.set_xticks(ticks)
	g.set_xticklabels(labels)
	plt.ylabel("Number of customers")
	plt.xlabel("")
	plt.show()
	plt.close()


def second_chart(data) -> None:
	df = pd.DataFrame(data, columns=["month", "amount"])
	df["month"] = df["month"].dt.strftime("%b")
	sns.barplot(
		data=df,
		x="month",
		y="amount",
		legend=False
	)
	plt.ylabel("total sales in million of A")
	plt.show()
	plt.close()


def third_chart(data) -> None:
	df = pd.DataFrame(data, columns=["date", "amount"])
	df["date"] = pd.to_datetime(df["date"])
	g = sns.lineplot(
		data=df,
		x="date",
		y="amount",
		legend=False
	)
	plt.fill_between(df["date"], df["amount"], alpha=0.3)
	monthly_ticks = df.groupby([df["date"].dt.year, df["date"].dt.month])["date"].min().sort_values()
	ticks = monthly_ticks.to_list()
	labels = [d.strftime("%b") for d in ticks]
	g.set_xticks(ticks)
	g.set_xticklabels(labels)
	plt.xlabel("")
	plt.ylabel("Number of customers")
	plt.show()
	plt.close()


def main():
	try:
		database = "postgresql://uwywijas:mysecretpassword@localhost:5432/piscineds"
		engine = sqla.create_engine(database)
		session = sqlaorm.sessionmaker(bind=engine)()
		query = sqla.text(read_sql_file("chart.1.sql"))
		result = session.execute(query)
		data = result.fetchall()
		sns.set_theme()
		first_chart(data)
		query = sqla.text(read_sql_file("chart.2.sql"))
		result = session.execute(query)
		data = result.fetchall()
		second_chart(data)
		query = sqla.text(read_sql_file("chart.3.sql"))
		result = session.execute(query)
		data = result.fetchall()
		third_chart(data)
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()


if __name__ == "__main__":
	main()
