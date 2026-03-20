"""CLI entrypoint for running the forex analysis from src package code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import run_analysis


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run forex analysis pipeline.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Directory containing fx_rate_daily.csv and interest_rate_daily.csv",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Optional output directory for CSV and JSON results",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = run_analysis(args.data_dir)

    print("ADF summary (GBP):")
    print(json.dumps(result["adf_summary"], indent=2))
    print("\nReturn correlations:")
    print(result["correlations"])

    if args.out_dir is not None:
        out_dir = args.out_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        result["major_pairs"].to_csv(out_dir / "major_pairs.csv", index=False)
        result["returns"].to_csv(out_dir / "returns.csv", index=False)
        result["correlations"].to_csv(out_dir / "correlations.csv")
        (out_dir / "adf_summary.json").write_text(
            json.dumps(result["adf_summary"], indent=2)
        )
        print(f"\nSaved outputs to: {out_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
