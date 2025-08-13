import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
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

def train_models(x: pd.DataFrame, y: pd.DataFrame):
	scaler = StandardScaler()
	x_scaled = scaler.fit_transform(x)
	model_tree = DecisionTreeClassifier(random_state=43)
	model_tree.fit(x_scaled, y)
	model_knn = KNeighborsClassifier(n_neighbors=12)
	model_knn.fit(x_scaled, y)
	model_lr = LogisticRegression(max_iter=1000, random_state=0)
	model_lr.fit(x_scaled, y)
	return scaler, (model_tree, model_knn, model_lr)

def show_models(x, y, test_x, test_y) -> None:
	k_values = np.arange(1, 31)
	scores = []
	scaler = StandardScaler()
	scaled_x = scaler.fit_transform(x)
	scaled_test_x = scaler.fit_transform(test_x)
	for k in k_values:
		knn = KNeighborsClassifier(n_neighbors=k)
		knn.fit(scaled_x, y)
		predictions = knn.predict(scaled_test_x)
		score = f1_score(test_y, predictions, average="weighted")
		scores.append(score)
	sns.lineplot(data=scores)
	plt.show()

def vote(predictions_0, predictions_1, predictions_2):
	predictions = []
	for index in range(len(predictions_0)):
		values = [predictions_0[index], predictions_1[index], predictions_2[index]]
		jedi = values.count(0)
		sith = values.count(1)
		predictions.append(1 if sith > jedi else 0)
	return predictions

def save_predictions(predictions) -> None:
	file_name: str = "Voting.txt"
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
		scaler, models = train_models(x, y)
		predictions_0 = models[0].predict(scaler.transform(test_x))
		predictions_1 = models[1].predict(scaler.transform(test_x))
		predictions_2 = models[2].predict(scaler.transform(test_x))
		predictions = vote(predictions_0, predictions_1, predictions_2)
		save_predictions(predictions)
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
