import argparse
import pandas as pd
from sklearn.preprocessing import StandardScaler


def normalize_features(input_csv, output_csv, target="compromised_controller_state"):
    df = pd.read_csv(input_csv)
    features = df.drop(columns=[target], errors="ignore")
    scaled = StandardScaler().fit_transform(features)
    out = pd.DataFrame(scaled, columns=features.columns)
    if target in df.columns:
        out[target] = df[target].values
    out.to_csv(output_csv, index=False)
    print(f"Normalized dataset saved to {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Normalize CAD feature columns")
    parser.add_argument("input_csv")
    parser.add_argument("-o", "--output", default="data/processed/cad_normalized.csv")
    args = parser.parse_args()
    normalize_features(args.input_csv, args.output)


if __name__ == "__main__":
    main()
