import pandas as pd
import seaborn as sns


DEFAULT_TRAIN_CSV_PATH = "../Train_knight.csv"


def generate_files(train_df):
	df_training = train_df.sample(n=int(train_df.shape[0] * 0.8), random_state=42)
	df_validation = train_df.drop(df_training.index)
	df_training.to_csv("Training_knight.csv", index=False)
	df_validation.to_csv("Validation_knight.csv", index=False)


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
		generate_files(train_df)
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main()
