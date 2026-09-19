from config import SYMBOL, TIMEFRAME

from data.rates import get_rates
from validation.rates_validation import validate_rates
from validation.gaps import detect_gaps
from storage.csv_storage import save_rates
from processing.analysis import analyze_rates, calculate_statistics
from visualization.charts import plot_drawdown, plot_price, plot_volatility
from research.volatility_regimes import (
    analyze_volatility_regimes,
    summarize_volatility_regimes,
    calculate_confidence_intervals,
)

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

    train_df, test_df = analyze_volatility_regimes(
        analyzed_df,
        horizon=24,
        train_ratio=0.7,
    )

    summary = summarize_volatility_regimes(test_df)
    confidence_intervals = calculate_confidence_intervals(test_df)

    print("\nVolatility Regime Research - Out of Sample")
    print(summary)

    print("\n95% Confidence Intervals")
    print(confidence_intervals)

    # Visualization
    # plot_price(analyzed_df)
    # plot_volatility(analyzed_df)
    # plot_drawdown(analyzed_df)

    stats = calculate_statistics(analyzed_df)

    print("\nMarket Statistics")

    for name, value in stats.items():
        print(f"{name}: {value}")