import pandas as pd

def backtest_low_volatility(
    df: pd.DataFrame,
    horizon: int = 24,
) -> pd.DataFrame:

    df = df.copy()

    trades = []

    i = 0

    while i < len(df) - horizon:

        if df.iloc[i]["volatility_regime"] == "low":

            entry_price = df.iloc[i]["close"]
            exit_price = df.iloc[i + horizon]["close"]

            strategy_return = (
                exit_price / entry_price
                - 1
            )

            trades.append({
                "entry_time": df.iloc[i]["time"],
                "exit_time": df.iloc[i + horizon]["time"],
                "entry_price": entry_price,
                "exit_price": exit_price,
                "return": strategy_return,
            })

            # Skip forward until the trade is closed
            i += horizon

        else:
            i += 1

    return pd.DataFrame(trades)

def calculate_strategy_statistics(
    df: pd.DataFrame,
) -> dict:

    trades = df["return"]

    if trades.empty:
        raise ValueError("No trades were generated")

    equity_curve = (1 + trades).cumprod()

    # Include starting equity of 1.0
    equity_with_start = pd.concat(
        [pd.Series([1.0]), equity_curve],
        ignore_index=True,
    )

    running_max = equity_with_start.cummax()
    drawdown = (
        equity_with_start / running_max - 1
    )

    return {
        "trades": len(trades),
        "total_return": equity_curve.iloc[-1] - 1,
        "mean_trade_return": trades.mean(),
        "median_trade_return": trades.median(),
        "positive_trade_pct": (trades > 0).mean(),
        "max_drawdown": drawdown.min(),
    }

def calculate_buy_and_hold_return(
    df: pd.DataFrame,
) -> float:

    start_price = df.iloc[0]["close"]
    end_price = df.iloc[-1]["close"]

    return end_price / start_price - 1

def calculate_exposure(
    df: pd.DataFrame,
    trades: pd.DataFrame,
) -> float:

    if trades.empty:
        return 0.0

    test_start = df.iloc[0]["time"]
    test_end = df.iloc[-1]["time"]

    total_hours = (
        test_end - test_start
    ).total_seconds() / 3600

    invested_hours = (
        trades["exit_time"] - trades["entry_time"]
    ).dt.total_seconds().sum() / 3600

    return invested_hours / total_hours

def build_equity_curves(
    df: pd.DataFrame,
    trades: pd.DataFrame,
) -> pd.DataFrame:

    result = df[["time", "close"]].copy()

    # Buy & Hold
    result["buy_hold_equity"] = (
        result["close"] / result.iloc[0]["close"]
    )

    # Strategy equity
    result["strategy_equity"] = 1.0

    equity = 1.0

    for _, trade in trades.iterrows():

        entry_time = trade["entry_time"]
        exit_time = trade["exit_time"]
        entry_price = trade["entry_price"]

        mask = (
            (result["time"] >= entry_time)
            & (result["time"] <= exit_time)
        )

        # Mark-to-market P&L while trade is open
        result.loc[mask, "strategy_equity"] = (
            equity
            * result.loc[mask, "close"]
            / entry_price
        )

        # Realized equity after exit
        exit_price = trade["exit_price"]

        equity *= exit_price / entry_price

        result.loc[
            result["time"] > exit_time,
            "strategy_equity",
        ] = equity

    return result

def calculate_equity_drawdown(
    equity_df: pd.DataFrame,
) -> dict:

    equity = equity_df["strategy_equity"]

    running_max = equity.cummax()

    drawdown = (
        equity / running_max - 1
    )

    return {
        "max_drawdown": drawdown.min(),
        "drawdown_series": drawdown,
    }
