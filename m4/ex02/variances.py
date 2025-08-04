import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def calc_variances(df: pd.DataFrame) -> None:
	df["knight"] = df["knight"].apply(lambda x: 1 if x == "Sith" else 0)

	df_standardized = (df - df.mean()) / df.std()
	pca = PCA()
	pca.fit(df_standardized)
	variances = pca.explained_variance_ratio_ * 100
	cumulative_variances = np.cumsum(variances)
	print("Variances (Percentage):\n", variances, "\n")
	print("Cumulative Variances (Percentage):\n", cumulative_variances)
	sns.lineplot(
		data=cumulative_variances,
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
		calc_variances(train_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main()
