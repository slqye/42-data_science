import pandas as pd
import seaborn as sns


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def check_default_csv_path(train_csv_path):
	if (train_csv_path == ""):
		return DEFAULT_TRAIN_CSV_PATH
	return train_csv_path


def covariance(data1, data2):
	# Cov(X, Y) = E[(Xi - mean(X))(Yi - mean(Y))] / n
	mean_x = data1.mean()
	mean_y = data2.mean()
	result = 0
	for i in range(len(data1)):
		result += (data1[i] - mean_x) * (data2[i] - mean_y)
	return result / len(data1)


def standard_deviation(data):
	# σ = sqrt(E[(Xi - mean(X))^2] / n)
	mean = data.mean()
	result = 0
	for i in range(len(data)):
		result += (data[i] - mean) ** 2
	return (result / len(data)) ** 0.5


def pearson_correlation(column1, column2):
	# Pxy: Cov(X, Y) / (σX * σY)
	covariance_value = covariance(column1, column2)
	standard_deviation_x = standard_deviation(column1)
	standard_deviation_y = standard_deviation(column2)
	return covariance_value / (standard_deviation_x * standard_deviation_y)


def print_correlations(df):
	df["knight"] = df["knight"].map({"Jedi": 1, "Sith": 0})
	values = sorted([
		(x, pearson_correlation(df["knight"], df[x]))
		for x in df.columns
	], key=lambda x: x[1], reverse=True)
	for i in values:
		if (i[1] > 0):
			format = "\t" if len(i[0]) < 8 else ""
			print(f"{i[0]}\t{format}{i[1]:.6f}")


def main():
	try:
		sns.set_theme()
		train_csv_path = check_default_csv_path(
			str(input("path \"Train_knight.csv\": "))
		)
		train_df = pd.read_csv(train_csv_path)
		print_correlations(train_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main()
