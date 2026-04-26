import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Print CAD model comparison table")
    parser.add_argument("--table", default="results/tables/cad_model_comparison.csv")
    args = parser.parse_args()
    df = pd.read_csv(args.table)
    print(df.sort_values("cv_accuracy_mean", ascending=False).to_string(index=False))


if __name__ == "__main__":
    main()
