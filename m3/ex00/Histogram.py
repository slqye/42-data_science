import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DEFAULT_TEST_CSV_PATH = "../Test_knight.csv"
DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def plot_test_histograms(df) -> None:
	rows: int = 6
	columns: int = 5
	fig, ax = plt.subplots(rows, columns, figsize=(15, 10))
	ax = ax.ravel()
	for i, column in enumerate(df.columns):
		sns.histplot(
			data=df,
			x=column,
			ax=ax[i],
			label="Knight",
			bins=40,
			color="green"
		)
		ax[i].set_title(column)
		ax[i].set_xlabel("")
		ax[i].set_ylabel("")
		ax[i].legend(loc="upper right")
	plt.tight_layout()
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
		# train_df = pd.read_csv(train_csv_path)
		plot_test_histograms(test_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main()
