import time
import pandas as pd
import sqlalchemy as sqla


def main():
	path: str = str(input("absolute csv path: "))
	start_time = time.time()
	try:
		df = pd.read_csv(path)
		database = "postgresql://uwywijas:mysecretpassword@localhost:5432/piscineds"
		engine = sqla.create_engine(database)
		metadata = sqla.MetaData()
		table_name = "items"
		metadata.create_all(engine)
		df.to_sql(table_name, engine, if_exists="replace", index=False, dtype={
			"product_id": sqla.Integer,
			"category_id": sqla.BigInteger,
			"category_code": sqla.String,
			"brand": sqla.String,
		})
	except Exception as e:
		print(f"error: {e}")
		return
	print(f"done in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
	main()
