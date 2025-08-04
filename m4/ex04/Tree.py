import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def calc_variances(df: pd.DataFrame) -> None:
	df["knight"] = df["knight"].apply(lambda x: 1 if x == "Sith" else 0)
	df_normalized = (df - df.min()) / (df.max() - df.min())
	features = ["Reactivity", "Push", "Survival", "Deflection"]
	x = df[features]
	y = df["knight"]
	dtree = DecisionTreeClassifier()
	dtree.fit(x, y)
	tree.plot_tree(
		dtree,
		feature_names=features,
	)
	plt.savefig("/mnt/c/Users/Slaye/Desktop/tree.png", dpi=600)


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
