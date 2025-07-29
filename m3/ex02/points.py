import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DEFAULT_TEST_CSV_PATH = "../Test_knight.csv"
DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def plot_charts(train_df, test_df) -> None:
	rows: int = 2
	columns: int = 2
	fig, ax = plt.subplots(rows, columns)
	palette = {"Sith": "red", "Jedi": "blue"}
	chart_00 = train_df[["Empowered", "Stims", "knight"]]
	sns.scatterplot(
		data=chart_00,
		x="Empowered",
		y="Stims",
		ax=ax[0, 0],
		hue="knight",
		palette=palette,
		alpha=0.5
	)
	ax[0, 0].set_xlabel("Empowered")
	ax[0, 0].set_ylabel("Stims")
	ax[0, 0].legend(loc="upper left")
	chart_10 = test_df[["Empowered", "Stims"]]
	sns.scatterplot(
		data=chart_10,
		x="Empowered",
		y="Stims",
		ax=ax[1, 0],
		color="green",
		label="Knight",
		alpha=0.5
	)
	ax[1, 0].set_xlabel("Empowered")
	ax[1, 0].set_ylabel("Stims")
	ax[1, 0].legend(loc="upper left")
	chart_01 = train_df[["Deflection", "Push", "knight"]]
	sns.scatterplot(
		data=chart_01,
		x="Push",
		y="Deflection",
		ax=ax[0, 1],
		hue="knight",
		palette=palette,
		alpha=0.5
	)
	ax[0, 1].set_xlabel("Push")
	ax[0, 1].set_ylabel("Deflection")
	ax[0, 1].legend(loc="upper right")
	chart_11 = test_df[["Deflection", "Push"]]
	sns.scatterplot(
		data=chart_11,
		x="Push",
		y="Deflection",
		ax=ax[1, 1],
		color="green",
		label="Knight",
		alpha=0.5
	)
	ax[1, 1].set_xlabel("Push")
	ax[1, 1].set_ylabel("Deflection")
	ax[1, 1].legend(loc="upper right")
	plt.tight_layout()
	plt.show()


def check_default_csv_path(test_csv_path, train_csv_path):
	if (test_csv_path == "") or (train_csv_path == ""):
		return DEFAULT_TEST_CSV_PATH, DEFAULT_TRAIN_CSV_PATH
	return test_csv_path, train_csv_path


def main():
	try:
		sns.set_theme()
		test_csv_path, train_csv_path = check_default_csv_path(
			str(input("path \"Test_knight.csv\": ")),
			str(input("path \"Train_knight.csv\": "))
		)
		test_df = pd.read_csv(test_csv_path)
		train_df = pd.read_csv(train_csv_path)
		plot_charts(train_df, test_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main()
