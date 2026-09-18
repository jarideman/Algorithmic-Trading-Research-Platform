import pandas as pd

def detect_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect missing hourly candles.

    Returns a DataFrame containing the time gaps.
    """
    df = df.sort_values("time").copy()

    df["time_diff"] = df["time"].diff()

    expected_interval = pd.Timedelta(hours=1)

    gaps = df[df["time_diff"] > expected_interval].copy()

    if gaps.empty:
        print("No missing hourly candles detected")
        return pd.DataFrame()

    gaps["missing_candles"] = (
        gaps["time_diff"] / expected_interval
    ).round().astype(int) - 1

    print(f"Detected {len(gaps)} time gaps")

    return gaps[
        ["time", "time_diff", "missing_candles"]
    ]
