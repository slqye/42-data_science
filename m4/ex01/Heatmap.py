import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def show_heatmap(df: pd.DataFrame) -> None:
	df["knight"] = df["knight"] == "Sith"
	sns.heatmap(
		df.corr()
	)
	plt.show()


def check_default_csv_path(train_csv_path):
	if train_csv_path == "":
		return DEFAULT_TRAIN_CSV_PATH
	return train_csv_path


def main():
	try:
		sns.set_theme()
		train_csv_path = check_default_csv_path(
			str(input("path \"Train_knight.csv\": "))
		)
		train_df = pd.read_csv(train_csv_path)
		show_heatmap(train_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main()
