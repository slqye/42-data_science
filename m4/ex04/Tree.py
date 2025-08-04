import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def decision_tree(df_train: pd.DataFrame, df_test: pd.DataFrame) -> None:
	df_train["knight"] = df_train["knight"].apply(lambda x: 1 if x == "Sith" else 0)
	features = ["Reactivity", "Push", "Survival", "Deflection"]
	x = df_train[features]
	y = df_train["knight"]
	dtree = DecisionTreeClassifier()
	dtree.fit(x, y)
	predictions = dtree.predict(df_test[features])
	with open("Tree.txt", "w") as file:
		for pred in predictions:
			file.write("Sith\n") if pred == 1 else file.write("Jedi\n")
	return
	tree.plot_tree(
		dtree,
		feature_names=features,
	)
	plt.show(dpi=600)


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
		decision_tree(train_df, test_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main(sys.argv)
