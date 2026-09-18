import MetaTrader5 as mt5
import pandas as pd
from config import SYMBOL, TIMEFRAME, CANDLE_COUNT

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