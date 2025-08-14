import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def calc_variances(df: pd.DataFrame) -> None:
	df["knight"] = df["knight"].apply(lambda x: 1 if x == "Sith" else 0)
	df_standardized = (df - df.mean()) / df.std()
	values = [
		(
			col,
			variance_inflation_factor(df_standardized, index),
			1 / variance_inflation_factor(df_standardized, index),
		)
		for index, col in enumerate(df.columns)
	]
	df_all = pd.DataFrame(values, columns=["Feature", "VIF", "Tolerance"])
	df_all.index = df_all["Feature"]
	df_all = df_all.drop(columns=["Feature"])
	print(df_all)
	print()
	values = [x for x in values if x[1] < 5]
	df_results = pd.DataFrame(values, columns=["Feature", "VIF", "Tolerance"])
	df_results.index = df_results["Feature"]
	df_results = df_results.drop(columns=["Feature"])
	print(df_results)


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
