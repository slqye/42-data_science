import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DEFAULT_TEST_CSV_PATH = "../Test_knight.csv"
DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def get_standardized_data(train_df, test_df):
	train_df["knight"] = train_df["knight"] == "Jedi"
	train_df["knight"] = train_df["knight"].map({True: 1, False: 0})

	train_max = train_df.max()
	train_min = train_df.min()
	test_max = test_df.max()
	test_min = test_df.min()
	train_df_normalized = (train_df - train_min) / (train_max - train_min)
	test_df_normalized = (test_df - test_min) / (test_max - test_min)
	print(train_df_normalized)
	print(test_df_normalized)

	train_df_normalized["knight"] = train_df["knight"].map({1: "Jedi", 0: "Sith"})
	chart = train_df_normalized[["Push", "Deflection", "knight"]]
	palette = {"Jedi": "blue", "Sith": "red"}
	sns.scatterplot(
		data=chart,
		x="Push",
		y="Deflection",
		hue="knight",
		palette=palette,
		alpha=0.5
	)
	plt.xlabel("Push")
	plt.ylabel("Deflection")
	plt.legend(title="")
	plt.show()
	plt.clf()
	test_df_normalized["knight"] = train_df["knight"].map({1: "Jedi", 0: "Sith"})
	chart = test_df_normalized[["Push", "Deflection"]]
	sns.scatterplot(
		data=chart,
		x="Push",
		y="Deflection",
		label="Knight",
		color="green",
		alpha=0.5
	)
	plt.xlabel("Push")
	plt.ylabel("Deflection")
	plt.legend(title="")
	plt.show()


def check_default_csv_path(test_csv_path, train_csv_path):
	if (test_csv_path == "") or (train_csv_path == ""):
		return DEFAULT_TEST_CSV_PATH, DEFAULT_TRAIN_CSV_PATH
	return test_csv_path, train_csv_path


def main():
	try:
		sns.set_theme()
		test_csv_path, train_csv_path = check_default_csv_path(
			str(input("path \"Test_knight.csv\": ")),
			str(input("path \"Train_knight.csv\": "))
		)
		test_df = pd.read_csv(test_csv_path)
		train_df = pd.read_csv(train_csv_path)
		get_standardized_data(train_df, test_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main()
