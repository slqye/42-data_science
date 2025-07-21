import time
import sqlalchemy as sqla
import sqlalchemy.orm as sqlaorm


def read_sql_file(path: str) -> str:
	data: str = ""
	with open(path, "r") as file:
		data = file.read().replace("\n", " ")
	return data


def main():
	start_time = time.time()
	try:
		print("combining items table on customers table")
		database = "postgresql://uwywijas:mysecretpassword@localhost:5432/piscineds"
		engine = sqla.create_engine(database)
		session = sqlaorm.sessionmaker(bind=engine)()
		query = sqla.text(read_sql_file("fusion.sql"))
		session.execute(query)
		session.commit()
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()
	print(f"done in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
	main()
