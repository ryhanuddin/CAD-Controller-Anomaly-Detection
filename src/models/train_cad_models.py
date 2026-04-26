import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

TARGET = "compromised_controller_state"


def get_models():
    return {
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=42),
        "KNN": Pipeline([("scaler", StandardScaler()), ("model", KNeighborsClassifier(n_neighbors=5))]),
        "SVM": Pipeline([("scaler", StandardScaler()), ("model", SVC(kernel="rbf", probability=True, random_state=42))]),
    }


def load_data(path):
    df = pd.read_csv(path).fillna(0)
    X = df.drop(columns=[TARGET])
    y = df[TARGET]
    return X, y


def train_all(data_path, model_dir, table_dir):
    X, y = load_data(data_path)
    model_dir = Path(model_dir)
    table_dir = Path(table_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)

    rows = []
    for name, model in get_models().items():
        scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rows.append({
            "model": name,
            "cv_accuracy_mean": scores.mean(),
            "cv_accuracy_std": scores.std(),
            "test_accuracy": accuracy_score(y_test, y_pred),
        })

        joblib.dump(model, model_dir / f"{name.lower()}_cad_model.joblib")
        print(f"\n{name}")
        print(f"CV accuracy: {scores.mean():.4f} ± {scores.std():.4f}")
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

    results = pd.DataFrame(rows)
    results.to_csv(table_dir / "cad_model_comparison.csv", index=False)
    print(f"\nSaved comparison table to {table_dir / 'cad_model_comparison.csv'}")


def main():
    parser = argparse.ArgumentParser(description="Train CAD classifiers")
    parser.add_argument("--data", default="data/processed/controller_identification_dataset_extended.csv")
    parser.add_argument("--model-dir", default="results/model_outputs")
    parser.add_argument("--table-dir", default="results/tables")
    args = parser.parse_args()
    train_all(args.data, args.model_dir, args.table_dir)


if __name__ == "__main__":
    main()
