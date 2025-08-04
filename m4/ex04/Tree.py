import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def decision_tree(df: pd.DataFrame) -> None:
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


def main(argv: list[str]) -> None:
	if len(argv) < 3:
		print("error: usage: python Tree.py <train_csv_path> <test_csv_path>")
		return
	try:
		sns.set_theme()
		train_df = pd.read_csv(argv[1])
		test_df = pd.read_csv(argv[2])
		decision_tree(train_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main(sys.argv)
