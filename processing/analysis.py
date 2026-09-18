import pandas as pd
import numpy as np

def analyze_rates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["return"] = df["close"].pct_change()
    df["log_return"] = np.log(
        df["close"] / df["close"].shift(1)
    )

    df["volatility_24h"] = (
        df["log_return"]
        .rolling(window=24)
        .std()
    )

    df["price_change"] = df["close"].diff()

    equity = df["close"] / df["close"].iloc[0]
    peak = equity.cummax()

    df["drawdown"] = equity / peak - 1

    return df

def calculate_statistics(
    df: pd.DataFrame
) -> dict:
    returns = df["return"].dropna()

    if returns.empty:
        raise ValueError("Not enough data to calculate statistics")

    # Cumulative return
    total_return = (
        (1 + returns).prod() - 1
    )

    # Calculate drawdown from close prices
    equity = (1 + returns).cumprod()
    peak = equity.cummax()
    drawdown = equity / peak - 1

    return {
        "total_return": total_return,
        "mean_return": returns.mean(),
        "std_return": returns.std(),
        "positive_return_pct": (returns > 0).mean(),
        "negative_return_pct": (returns < 0).mean(),
        "max_drawdown": drawdown.min(),
        "observations": len(returns),
    }