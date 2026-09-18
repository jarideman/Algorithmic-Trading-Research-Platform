
import pandas as pd


def validate_rates(df: pd.DataFrame) -> bool:
    if df is None or df.empty:
        print("Validation failed: DataFrame is empty")
        return False

    required_columns = [
        "time",
        "open",
        "high",
        "low",
        "close",
        "tick_volume",
        "spread",
        "real_volume",
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return False

    if df[required_columns].isnull().any().any():
        print("Validation failed: Missing values found")
        return False

    if df["time"].duplicated().any():
        print("Validation failed: Duplicate timestamps")
        return False

    if not df["time"].is_monotonic_increasing:
        print("Validation failed: Data is not sorted")
        return False

    invalid_ohlc = (
        (df["high"] < df["low"])
        | (df["high"] < df["open"])
        | (df["high"] < df["close"])
        | (df["low"] > df["open"])
        | (df["low"] > df["close"])
    )

    if invalid_ohlc.any():
        print("Validation failed: Invalid OHLC values")
        return False

    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        print("Validation failed: Non-positive prices")
        return False

    print("Validation successful")
    return True