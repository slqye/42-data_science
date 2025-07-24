import sqlalchemy as sqla
import sqlalchemy.orm as sqlaorm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random


def read_sql_file(path: str) -> str:
	data: str = ""
	with open(path, "r") as file:
		data = file.read().replace("\n", " ")
	return data


def k_means(data: list, k: int, states: int) -> list:
	data_length = len(data)
	result = []
	for i in range(states):
		state_result = {}
		# Initialize the state result with empty lists for each k
		for i in range(k):
			state_result[i] = []
		# Randomly select k points from the data
		k_points_index = random.sample(range(data_length), k)
		# Looping through each point in the data
		for current_point_index in range(data_length):
			distances = []
			current_point = data[current_point_index]
			# Calculate the distance from the current point to each of the k points
			for k_point_index in k_points_index:
				k_point = data[k_point_index]
				# Euclidean distance calculation
				distances.append(((k_point[0] - current_point[0]) ** 2+ (current_point[1] - k_point[1]) ** 2) ** 0.5)
			# Append the current point to the kluster with the smallest distance
			state_result[distances.index(min(distances))].append(current_point_index)
		for i in range(k):
			state_result[i] = len(state_result[i])
		result.append(state_result)
	return result


def users_chart(data) -> None:
	df = pd.DataFrame(data, columns=["purchases", "total_spent"])
	for i in range(1, 11):
		means = k_means(df.values.tolist(), i, 42)
		for j in means:
			print(f"state {means.index(j) + 1}: {j}")
		print()
	return
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
