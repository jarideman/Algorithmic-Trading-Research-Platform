from config import SYMBOL, TIMEFRAME

from data.rates import get_rates
from validation.rates_validation import validate_rates
from validation.gaps import detect_gaps
from storage.csv_storage import save_rates
from processing.analysis import analyze_rates, calculate_statistics


def run_market_data_pipeline():
    df = get_rates()

    if df is None:
        return

    if not validate_rates(df):
        return

    df = df.sort_values("time").reset_index(drop=True)

    gaps = detect_gaps(df)

    if not gaps.empty:
        print(f"Warning: {len(gaps)} gaps detected")
    else:
        print("No missing hourly candles detected")

    save_rates(df, SYMBOL, TIMEFRAME)

    analyzed_df = analyze_rates(df)

    stats = calculate_statistics(analyzed_df)

    print("\nMarket Statistics")

    for name, value in stats.items():
        print(f"{name}: {value}")