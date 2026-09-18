import MetaTrader5 as mt5
import pandas as pd
import config

from connection.mt5_connection import init_mt5, deinit_mt5
from validation.rates_validation import validate_rates
from validation.gaps import detect_gaps
from storage.csv_storage import save_rates
from processing.analysis import (
    analyze_rates,
    calculate_statistics,
)

SYMBOL = config.SYMBOL
TIMEFRAME = config.TIMEFRAME
CANDLE_COUNT = config.CANDLE_COUNT

def main():
    if not init_mt5():
        return

    try:
        df = get_rates()

        if df is not None and validate_rates(df):

            df = df.sort_values("time").reset_index(drop=True)

            detect_gaps(df)

            save_rates(df, SYMBOL, TIMEFRAME)

            analyzed_df = analyze_rates(df)

            stats = calculate_statistics(analyzed_df)

            print("\nMarket Statistics")

            for name, value in stats.items():
                print(f"{name}: {value}")

            analyzed_df.to_csv(
                "data/processed/BTCUSD_H1_analysis.csv",
                index=False
            )

    finally:
        deinit_mt5()

def get_rates():
    rates = mt5.copy_rates_from_pos(
        SYMBOL,
        TIMEFRAME,
        0,
        CANDLE_COUNT
    )

    if rates is None:
        print(f"Failed to retrieve rates: {mt5.last_error()}")
        return None

    if len(rates) == 0:
        print("No rates received")
        return None

    df = pd.DataFrame(rates)

    df["time"] = pd.to_datetime(
        df["time"],
        unit="s",
        utc=True
    )

    print(f"Retrieved {len(df)} candles for {SYMBOL}")

    return df

if __name__ == "__main__":
    main()
