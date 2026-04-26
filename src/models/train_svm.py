import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

TARGET = "compromised_controller_state"

from sklearn.svm import SVC


def main():
    parser = argparse.ArgumentParser(description="Train SVM for CAD")
    parser.add_argument("--data", default="data/processed/controller_identification_dataset_extended.csv")
    parser.add_argument("--output", default="results/model_outputs/svm_cad_model.joblib")
    args = parser.parse_args()

    df = pd.read_csv(args.data).fillna(0)
    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    model = Pipeline([("scaler", StandardScaler()), ("model", SVC(kernel="rbf", probability=True, random_state=42))])
    scores = cross_val_score(model, X, y, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42))
    model.fit(X, y)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.output)
    print(f"Accuracy: {scores.mean():.4f} ± {scores.std():.4f}")
    print(f"Saved model to {args.output}")


if __name__ == "__main__":
    main()
