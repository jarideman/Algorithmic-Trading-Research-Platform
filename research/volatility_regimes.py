import pandas as pd
import numpy as np

def analyze_volatility_regimes(
    df: pd.DataFrame,
    horizon: int = 24,
    train_ratio: float = 0.7,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    df = df.copy()

    # Remove rows where rolling volatility is not available
    df = df.dropna(subset=["volatility_24h"]).reset_index(drop=True)

    if len(df) <= horizon:
        raise ValueError("Not enough data for the selected horizon")

    # Chronological train/test split
    split_index = int(len(df) * train_ratio)

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    # Calculate thresholds ONLY on training data
    low_threshold = train_df["volatility_24h"].quantile(0.33)
    high_threshold = train_df["volatility_24h"].quantile(0.67)

    # Apply thresholds to training data
    train_df["volatility_regime"] = "medium"

    train_df.loc[
        train_df["volatility_24h"] <= low_threshold,
        "volatility_regime"
    ] = "low"

    train_df.loc[
        train_df["volatility_24h"] >= high_threshold,
        "volatility_regime"
    ] = "high"

    # Apply the SAME thresholds to test data
    test_df["volatility_regime"] = "medium"

    test_df.loc[
        test_df["volatility_24h"] <= low_threshold,
        "volatility_regime"
    ] = "low"

    test_df.loc[
        test_df["volatility_24h"] >= high_threshold,
        "volatility_regime"
    ] = "high"

    # Forward return over the selected horizon
    test_df["forward_return"] = (
        test_df["close"].shift(-horizon) / test_df["close"] - 1
    )

    # Remove rows without a complete forward horizon
    test_df = test_df.dropna(subset=["forward_return"])

    return train_df, test_df

def summarize_volatility_regimes(
    df: pd.DataFrame,
) -> pd.DataFrame:

    summary = (
        df.groupby("volatility_regime")["forward_return"]
        .agg(
            observations="count",
            mean_return="mean",
            median_return="median",
            std_return="std",
            min_return="min",
            max_return="max",
        )
    )

    summary["positive_return_pct"] = (
        df.groupby("volatility_regime")["forward_return"]
        .apply(lambda returns: (returns > 0).mean())
    )

    summary["return_below_minus_2_pct"] = (
        df.groupby("volatility_regime")["forward_return"]
        .apply(lambda returns: (returns < -0.02).mean())
    )

    return summary

def calculate_confidence_intervals(
    df: pd.DataFrame,
) -> pd.DataFrame:

    results = []

    for regime, group in df.groupby("volatility_regime"):
        returns = group["forward_return"].dropna()

        mean = returns.mean()
        std = returns.std()
        n = len(returns)

        standard_error = std / np.sqrt(n)

        lower = mean - 1.96 * standard_error
        upper = mean + 1.96 * standard_error

        results.append({
            "volatility_regime": regime,
            "mean_return": mean,
            "ci_lower": lower,
            "ci_upper": upper,
        })

    return pd.DataFrame(results).set_index("volatility_regime")
