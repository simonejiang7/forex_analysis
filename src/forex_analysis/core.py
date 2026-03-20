"""Core helpers for forex market notebook workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def package_name() -> str:
    """Return the package name for a simple import smoke check."""
    return "forex_analysis"


def load_csv(path: str | Path):
    """Load a CSV file into a dataframe."""
    import pandas as pd

    return pd.read_csv(path)


def drop_missing_rows(df, required_columns: Iterable[str]):
    """Drop rows where required columns are missing."""
    return df.dropna(subset=list(required_columns))


def adf_summary(series) -> dict[str, float]:
    """Return a minimal ADF stationarity summary."""
    from statsmodels.tsa.stattools import adfuller

    statistic, pvalue, *_ = adfuller(series.dropna())
    return {"adf_statistic": float(statistic), "p_value": float(pvalue)}


def log_diff_returns(df, columns: Iterable[str]):
    """Compute log-difference returns for selected columns."""
    import numpy as np

    cols = list(columns)
    return np.log(df[cols]).diff().dropna()


def correlations(df, columns: Iterable[str]):
    """Correlation matrix for selected columns."""
    cols = list(columns)
    return df[cols].corr()


def prepare_major_pairs(
    fx_df,
    date_column: str = "date",
):
    """Select and rename major pairs: EUR/USD, GBP/USD, CHF/USD."""
    required = [date_column, "dexeuus", "dexukus", "dexszus"]
    cleaned = drop_missing_rows(fx_df, required).sort_values(by=date_column)
    return cleaned[required].rename(
        columns={"dexeuus": "eur", "dexukus": "gbp", "dexszus": "chf"}
    )


def run_analysis(data_dir: str | Path):
    """Run the core analysis flow and return main outputs."""
    data_path = Path(data_dir)
    fx = load_csv(data_path / "fx_rate_daily.csv")
    _ = load_csv(data_path / "interest_rate_daily.csv")

    major_pairs = prepare_major_pairs(fx)
    returns = log_diff_returns(major_pairs, ["eur", "gbp", "chf"])
    corr = correlations(returns, ["eur", "gbp", "chf"])
    adf = adf_summary(major_pairs["gbp"])

    return {
        "major_pairs": major_pairs,
        "returns": returns,
        "correlations": corr,
        "adf_summary": adf,
    }
