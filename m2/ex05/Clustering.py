import sqlalchemy as sqla
import sqlalchemy.orm as sqlaorm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np


def read_sql_file(path: str) -> str:
	data: str = ""
	with open(path, "r") as file:
		data = file.read().replace("\n", " ")
	return data


def k_means(data: list, k: int, k_center) -> list:
	data_length = len(data)
	result = {}
	# Randomly select k points from the data
	k_points = random.sample(range(data_length), k)
	# Convert the indices to actual data points
	for j in k_points:
		k_points[k_points.index(j)] = data[j]
	# Ajusting the k points to be unique and centered
	for j in range(k_center):
		# Initialize the state result with empty lists for each k
		for m in range(k):
			result[m] = []
		# Looping through each point in the data
		for current_point_index in range(data_length):
			distances = []
			current_point = data[current_point_index]
			# Calculate the distance from the current point to each of the k points
			for kluster in k_points:
				# Euclidean distance calculation
				distances.append(((kluster[0] - current_point[0]) ** 2 + (current_point[1] - kluster[1]) ** 2) ** 0.5)
			# Append the current point to the kluster with the smallest distance
			result[distances.index(min(distances))].append(current_point_index)
		# Calculate the new k points as the mean of the points in each kluster
		for kluster_index in range(len(k_points)):
			if len(result[kluster_index]) > 0:
				mean_x = sum([data[index][0] for index in result[kluster_index]]) / len(result[kluster_index])
				mean_y = sum([data[index][1] for index in result[kluster_index]]) / len(result[kluster_index])
				k_points[kluster_index] = (mean_x, mean_y)
	return result, k_points


def customers_type_count_chart(data) -> None:
	df = pd.DataFrame(data, columns=["purchases", "total_spent"])
	k_result = k_means(df.values.tolist(), 3, 42)
	type_count = [len(x) for x in k_result[0].values()]
	k_center = k_result[1]
	k_center_dist = [x[0] ** 2 + x[1] ** 2 for x in k_center]
	types = {
		"Small customers": type_count[k_center_dist.index(min(k_center_dist))],
		"Medium customers": type_count[k_center_dist.index(sorted(k_center_dist)[1])],
		"Big customers": type_count[k_center_dist.index(max(k_center_dist))]
	}
	type_df = pd.DataFrame(types.items(), columns=["type", "customers"])
	sns.barplot(
		data=type_df,
		x="customers",
		y="type",
		hue="type",
		legend=False
	)
	for i, value in enumerate(type_df["customers"]):
		plt.text(value + 0.5, i, str(value), va="center")
	plt.ylabel("")
	plt.show()
	plt.close()


def k_center_chart(data) -> None:
	df = pd.DataFrame(
		data,
		columns=["purchases_per_months", "events_times", "total_spent"]
	)
	df_means = pd.DataFrame({
		"ppm": df["purchases_per_months"],
		"recency": df["events_times"]
	})
	df_means["recency"] = df_means["recency"].apply(
		lambda x: np.mean(
			[(x[y + 1] - x[y]).total_seconds() for y in range(len(x) - 1)]
		) if len(x) > 1 else (1 / 5)
	)
	print(df_means.head(25))
	k_result = k_means(df_means.values.tolist(), 3, 10)
	k_center = k_result[1]
	k_df = pd.DataFrame(k_center, columns=["purchases_per_months", "recency"])
	sns.relplot(
		data=df_means,
		x="recency",
		y="ppm",
		legend=False,
	)
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
		# customers_type_count_chart(get_data(session, "Clustering.1.sql"))
		k_center_chart(get_data(session, "Clustering.1.sql"))
	except Exception as e:
		print(f"error: {e}")
		return
	finally:
		session.close()
		engine.dispose()


if __name__ == "__main__":
	main()
