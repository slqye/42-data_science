import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"
POSITIVE_LABEL = "Jedi"

def train_model(x: pd.DataFrame, y: pd.DataFrame):
	model = DecisionTreeClassifier(random_state=10)
	model.fit(x, y)
	return model

def format_data(df_train: pd.DataFrame, df_test: pd.DataFrame):
	df_train["knight"] = df_train["knight"].map({"Jedi": 1, "Sith": 0})
	y = df_train["knight"]
	x = df_train.drop("knight", axis=1)
	test_data = None
	if "knight" in df_test.columns:
		test_data = df_test["knight"].drop("knight", axis=1)
	else:
		test_data = df_test
	return x, y, test_data

def test_model(model, test_data) -> None:
	predictions = model.predict(test_data)
	save_predictions(predictions)

def save_predictions(predictions) -> None:
	file_name: str = "Tree.txt"
	with open(file_name, "w", encoding="UTF-8") as file:
		for pred in predictions:
			file.write("Sith\n" if pred == 1 else "Jedi\n")

def get_accuracy(prediction: str, truth: str) -> None:
	tp: int = 0
	tn: int = 0
	fp: int = 0
	fn: int = 0

	with open(prediction, "r", encoding="UTF-8") as pred_file, open(truth, "r") as truth_file:
		for pred_line, truth_line in zip(pred_file, truth_file):
			pred_value = str(pred_line.strip())
			truth_value = str(truth_line.strip())
			if pred_value == truth_value:
				if pred_value == POSITIVE_LABEL:
					tp += 1
				else:
					tn += 1
			elif pred_value == POSITIVE_LABEL:
				fp += 1
			else:
				fn += 1
	jedi_precision = tp / (tp + fp)
	sith_precision = tn / (tn + fn)
	jedi_recall = tp / (tp + fn)
	sith_recall = tn / (tn + fp)
	jedi_f1 = 2 * (jedi_precision * jedi_recall) / (jedi_precision + jedi_recall)
	sith_f1 = 2 * (sith_precision * sith_recall) / (sith_precision + sith_recall)
	jedi_total = tp + fn
	sith_total = tn + fp
	accuracy = (tp + tn) / (tp + tn + fp + fn)
	total = jedi_total + sith_total

	print("\tprecision\trecall\tf1-score\ttotal")
	print(f"Jedi\t{jedi_precision:.2f}\t\t{jedi_recall:.2f}\t{jedi_f1:.2f}\t\t{jedi_total}")
	print(f"Sith\t{sith_precision:.2f}\t\t{sith_recall:.2f}\t{sith_f1:.2f}\t\t{sith_total}")
	print()
	print(f"accuracy\t\t\t{accuracy}\t\t{total}")

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
		x, y, test_data = format_data(train_df, test_df)
		model = train_model(x, y)
		test_model(model, test_data)
		get_accuracy("Tree.txt", "truth.txt")
	except Exception as e:
		print(f"error: {e}")
		return

if __name__ == "__main__":
	main(sys.argv)
