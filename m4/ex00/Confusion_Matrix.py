import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


POSITIVE_LABEL = "Jedi"


def calculate_confusion_matrix(predictions: str, truth: str):
	tp: int = 0
	tn: int = 0
	fp: int = 0
	fn: int = 0

	with open(predictions, "r") as pred_file, open(truth, "r") as truth_file:
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
	matrix = [
		[tp, fn],
		[fp, tn]
	]
	print("\tprecision\trecall\tf1-score\ttotal")
	print(f"Jedi\t{jedi_precision:.2f}\t\t{jedi_recall:.2f}\t{jedi_f1:.2f}\t\t{jedi_total}")
	print(f"Sith\t{sith_precision:.2f}\t\t{sith_recall:.2f}\t{sith_f1:.2f}\t\t{sith_total}")
	print()
	print(f"accuracy\t\t\t{accuracy}\t\t{total}")
	print()
	print(matrix)
	sns.heatmap(
		matrix,
		annot=True,
		cmap="viridis",
	)
	plt.show()


def main(argv: list) -> None:
	if len(argv) != 3:
		print("usage: python Confusion_Matrix.py <predictions.txt> <truth.txt>")
		return
	try:
		sns.set_theme()
		calculate_confusion_matrix(argv[1], argv[2])
	except Exception as e:
		print(f"error: {e}")
		return


if __name__ == "__main__":
	main(sys.argv)
