import os
import time
import pandas as pd
import sqlalchemy as sqla


def add_table(engine, path: str):
	try:
		df = pd.read_csv(path)
		metadata = sqla.MetaData()
		table_name = path.split("/")[-1].split(".")[0]
		metadata.create_all(engine)
		df.to_sql(table_name, engine, if_exists="replace", index=False, dtype={
			"event_time": sqla.DateTime,
			"event_type": sqla.String,
			"product_id": sqla.Integer,
			"price": sqla.Float,
			"user_id": sqla.BigInteger,
			"user_session": sqla.String(length=36)
		})
	except Exception as e:
		print(f"error: {e}")
		return


def main():
	start_time = time.time()
	try:
		path = str(input("absolute customer folder path: "))
		database = "postgresql://uwywijas:mysecretpassword@localhost:5432/piscineds"
		engine = sqla.create_engine(database)
		files = os.listdir(path)
		for file in files:
			if file.endswith(".csv"):
				file_path = os.path.join(path, file)
				print(f"adding table from {file_path}")
				add_table(engine, file_path)
	except Exception as e:
		print(f"error: {e}")
		return
	print(f"done in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
	main()
