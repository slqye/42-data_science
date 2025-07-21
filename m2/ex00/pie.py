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
		length = len(data)
		dataframe = {
			"view": data.count(("view",)) * 100 / length,
			"purchase": data.count(("purchase",)) * 100 / length,
			"remove_from_cart": data.count(("remove_from_cart",)) * 100 / length,
			"cart": data.count(("cart",)) * 100 / length,
		}
		df = pd.DataFrame(dataframe.items())
		print(df)
		# sns.relplot(df, kind="pie")
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()


if __name__ == "__main__":
	main()
