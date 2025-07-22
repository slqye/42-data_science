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
		legend=False
	)
	months = df["date"].dt.month.unique()
	months_days = [
		[y for y in df["date"].dt.month].count(x)
		for x in months
	]
	ticks = [
		sum([months_days[y] for y in range(x)])
		for x in range(len(months_days))
	]
	g.set_xticks(ticks)
	g.set_xticklabels([calendar.month_abbr[x] for x in months])
	plt.ylabel("Number of customers")
	plt.show()


def main():
	try:
		database = "postgresql://uwywijas:mysecretpassword@localhost:5432/piscineds"
		engine = sqla.create_engine(database)
		session = sqlaorm.sessionmaker(bind=engine)()
		query = sqla.text(read_sql_file("chart.1.sql"))
		result = session.execute(query)
		session.commit()
		data = result.fetchall()
		sns.set_theme()
		first_chart(data)
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()


if __name__ == "__main__":
	main()
