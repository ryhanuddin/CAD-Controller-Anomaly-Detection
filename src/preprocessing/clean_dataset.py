import argparse
import pandas as pd


def clean_dataset(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df = df.drop_duplicates()
    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.fillna(0)
    df.to_csv(output_csv, index=False)
    print(f"Cleaned dataset saved to {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Clean CAD dataset")
    parser.add_argument("input_csv")
    parser.add_argument("-o", "--output", default="data/processed/cad_clean.csv")
    args = parser.parse_args()
    clean_dataset(args.input_csv, args.output)


if __name__ == "__main__":
    main()
