import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def calc_variances(df: pd.DataFrame) -> None:
	df["knight"] = df["knight"] == "Sith"
	variances = []
	cumulative_variances = []
	for i in df.columns:
		variances.append(df[i].var())
	for i in range(len(variances)):
		if i == 0:
			cumulative_variances.append(variances[i])
		else:
			cumulative_variances.append(cumulative_variances[i - 1] + variances[i])
	print("Variances (Percentage):\n", variances)
	print()
	print("Cumulative Variances (Percentage):\n", cumulative_variances)


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
		calc_variances(train_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main()
