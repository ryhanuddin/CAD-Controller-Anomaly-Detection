import argparse
from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

TARGET = "compromised_controller_state"


def main():
    parser = argparse.ArgumentParser(description="Plot confusion matrix for a CAD model")
    parser.add_argument("--data", default="data/processed/controller_identification_dataset_extended.csv")
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", default="results/figures/confusion_matrix.png")
    args = parser.parse_args()

    df = pd.read_csv(args.data).fillna(0)
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)

    model = joblib.load(args.model)
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(args.output, dpi=300)
    print(f"Saved figure to {args.output}")


if __name__ == "__main__":
    main()
