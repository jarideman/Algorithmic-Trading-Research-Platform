import pandas as pd
import numpy as np

def analyze_rates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Calculate hourly percentage returns
    df["return"] = df["close"].pct_change()

    # Calculate logarithmic returns
    df["log_return"] = np.log(
        df["close"] / df["close"].shift(1)
    )

    # Rolling volatility over 24 candles
    df["volatility_24h"] = (
        df["log_return"]
        .rolling(window=24)
        .std()
    )

    # Calculate price change
    df["price_change"] = df["close"].diff()

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