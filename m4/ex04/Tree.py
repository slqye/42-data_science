import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score

DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"
POSITIVE_LABEL = "Jedi"

def format_data(df_train: pd.DataFrame, df_test: pd.DataFrame):
	df_train["knight"] = df_train["knight"].map({"Jedi": 1, "Sith": 0})
	if "knight" in df_test.columns:
		df_test["knight"] = df_test["knight"].map({"Jedi": 1, "Sith": 0})
	y = df_train["knight"]
	x = df_train.drop("knight", axis=1)
	test_y = df_test["knight"] if "knight" in df_test.columns else None
	test_x = df_test.drop("knight", axis=1) if "knight" in df_test.columns else df_test
	return x, y, test_x, test_y

def train_model(x: pd.DataFrame, y: pd.DataFrame):
	model = DecisionTreeClassifier(random_state=11)
	model.fit(x, y)
	return model

def show_model(model, x) -> None:
	plt.figure(figsize=(20, 10))
	plot_tree(model, filled=True, feature_names=x.columns)
	plt.show()

def save_predictions(predictions) -> None:
	file_name: str = "Tree.txt"
	with open(file_name, "w", encoding="UTF-8") as file:
		for pred in predictions:
			file.write("Sith\n" if pred == 1 else "Jedi\n")

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
		x, y, test_x, test_y = format_data(train_df, test_df)
		model = train_model(x, y)
		predictions = model.predict(test_x)
		save_predictions(predictions)
		# show_model(model, x)
		if test_y is None:
			raise ValueError("warning: f1_score unknown (not a validation set)")
		model_f1_score = f1_score(test_y, predictions)
		print(f"f1_score: {model_f1_score * 100:.2f}%")
	except ValueError as e:
		print(e)
	except Exception as e:
		print(f"error: {e}")


if __name__ == "__main__":
	main(sys.argv)
