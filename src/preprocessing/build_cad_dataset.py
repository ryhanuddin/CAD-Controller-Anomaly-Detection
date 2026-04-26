import argparse
import pandas as pd
from feature_extraction import extract_window_features


def build_dataset(input_csv, output_csv, window_size=5000):
    df = pd.read_csv(input_csv)
    rows = []
    for start in range(0, len(df), window_size):
        window = df.iloc[start:start + window_size]
        if not window.empty:
            rows.append(extract_window_features(window))
    pd.DataFrame(rows).to_csv(output_csv, index=False)
    print(f"Saved {len(rows)} CAD windows to {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Build CAD feature windows from OpenFlow CSV")
    parser.add_argument("input_csv")
    parser.add_argument("-o", "--output", default="data/processed/cad_features.csv")
    parser.add_argument("--window-size", type=int, default=5000)
    args = parser.parse_args()
    build_dataset(args.input_csv, args.output, args.window_size)


if __name__ == "__main__":
    main()
