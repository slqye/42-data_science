import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score

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
	model = KNeighborsClassifier(n_neighbors=5)
	model.fit(x, y)
	return model

def show_models(x, y) -> None:
	k_values = np.arange(1, 31)
	scores = []
	scaler = StandardScaler()
	scaled_x = scaler.fit_transform(x)
	for k in k_values:
		knn = KNeighborsClassifier(n_neighbors=k)
		score = cross_val_score(knn, scaled_x, y, cv=2)
		scores.append(score[0])
	sns.lineplot(data=scores)
	plt.show()

def save_predictions(predictions) -> None:
	file_name: str = "KNN.txt"
	with open(file_name, "w", encoding="UTF-8") as file:
		for pred in predictions:
			file.write("Sith\n" if pred == 1 else "Jedi\n")

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
		if test_y is None:
			raise ValueError("warning: f1_score unknown (not a validation set)")
		show_models(x, y)
	except ValueError as e:
		print(e)
	except Exception as e:
		print(f"error: {e}")


if __name__ == "__main__":
	main(sys.argv)
