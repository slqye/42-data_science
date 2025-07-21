import time
import sqlalchemy as sqla
import sqlalchemy.orm as sqlaorm


def main():
	start_time = time.time()
	try:
		database = "postgresql://uwywijas:mysecretpassword@localhost:5432/piscineds"
		engine = sqla.create_engine(database)
		session = sqlaorm.sessionmaker(bind=engine)()
		tables = sqla.inspect(engine).get_table_names()
		tables = [table for table in tables if table.startswith("data_202")]
		query = "CREATE TABLE IF NOT EXISTS customers AS " + " UNION ALL ".join(
			[f"SELECT * FROM {table}" for table in tables]) + ";"
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
