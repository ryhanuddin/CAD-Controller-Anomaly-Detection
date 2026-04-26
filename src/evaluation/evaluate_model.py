import argparse
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

TARGET = "compromised_controller_state"


def main():
    parser = argparse.ArgumentParser(description="Evaluate a saved CAD model")
    parser.add_argument("--data", default="data/processed/controller_identification_dataset_extended.csv")
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.data).fillna(0)
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)

    model = joblib.load(args.model)
    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    main()
