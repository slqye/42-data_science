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


def main():
	sns.set_theme()
	try:
		database = "postgresql://uwywijas:mysecretpassword@localhost:5432/piscineds"
		engine = sqla.create_engine(database)
		session = sqlaorm.sessionmaker(bind=engine)()
		query = sqla.text(read_sql_file("pie.sql"))
		result = session.execute(query)
		session.commit()
		data = result.fetchall()
		length = sum([int(x[1]) for x in data])
		numbers = [int(x[1] * 100) for x in data]
		values = {
			"view": numbers[3] / length,
			"cart": numbers[0] / length,
			"remove_from_cart": numbers[2] / length,
			"purchase": numbers[1] / length
		}
		colors = sns.color_palette('pastel')[0:4]
		plt.pie(
			values.values(),
			labels=values.keys(),
			autopct='%1.1f%%',
			colors=colors,
		)
		plt.show()
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()


if __name__ == "__main__":
	main()
