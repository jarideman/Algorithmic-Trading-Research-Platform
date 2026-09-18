import MetaTrader5 as mt5
import pandas as pd
from validation.rates_validation import validate_rates
from validation.gaps import detect_gaps
from storage.csv_storage import save_rates
import config

SYMBOL = config.SYMBOL
TIMEFRAME = config.TIMEFRAME
CANDLE_COUNT = config.CANDLE_COUNT

def main():
    if not init_mt5():
        return

    try:
        df = get_rates()

        if df is not None and validate_rates(df):

            gaps = detect_gaps(df)

            if not gaps.empty:
                print(gaps.to_string(index=False))

            save_rates(
                df,
                symbol=SYMBOL,
                timeframe="H1"
            )

    finally:
        deinit_mt5()

def init_mt5():
    if not mt5.initialize():
        print('MT5 initialization failed')
        return False

    if not mt5.symbol_select(SYMBOL, True):
        print('Symbol not found')
        deinit_mt5()
        return False

    print('MT5 initialization successful')
    return True

def deinit_mt5():
    mt5.shutdown()
    return

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
