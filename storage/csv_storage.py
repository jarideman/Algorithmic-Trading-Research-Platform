from pathlib import Path

import pandas as pd

def save_rates(df: pd.DataFrame, symbol: str, timeframe: str):
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{symbol}_{timeframe}.csv"
    output_path = output_dir / filename

    df.to_csv(output_path, index=False)

    print(f"Saved {len(df)} candles to {output_path}")

    return output_path
