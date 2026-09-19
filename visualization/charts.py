import matplotlib.pyplot as plt
import pandas as pd

def plot_price(df: pd.DataFrame):
    plt.figure(figsize=(12, 6))

    plt.plot(df["time"], df["close"])

    plt.title("BTCUSD Closing Price")
    plt.xlabel("Time")
    plt.ylabel("Price")

    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_volatility(df: pd.DataFrame):
    plt.figure(figsize=(12, 6))

    plt.plot(df["time"], df["volatility_24h"])

    plt.title("BTCUSD Rolling Volatility")
    plt.xlabel("Time")
    plt.ylabel("Volatility")

    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_drawdown(df: pd.DataFrame):
    plt.figure(figsize=(12, 6))

    plt.plot(df["time"], df["drawdown"])

    plt.title("BTCUSD Drawdown")
    plt.xlabel("Time")
    plt.ylabel("Drawdown")

    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_equity_curve(df: pd.DataFrame) -> None:
    plt.figure(figsize=(12, 6))

    plt.plot(
        df["time"],
        df["strategy_equity"],
        label="Low Volatility Strategy",
    )

    plt.plot(
        df["time"],
        df["buy_hold_equity"],
        label="Buy & Hold",
    )

    plt.title("Strategy vs Buy & Hold")
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.legend()
    plt.grid(True)

    plt.show()

def plot_drawdown_curve(df: pd.DataFrame) -> None:

    equity = df["strategy_equity"]

    running_max = equity.cummax()

    drawdown = (
        equity / running_max - 1
    )

    max_drawdown = drawdown.min()

    plt.figure(figsize=(12, 5))

    plt.plot(
        df["time"],
        drawdown * 100,
        label="Strategy Drawdown",
    )

    plt.axhline(
        0,
        linewidth=1,
    )

    plt.axhline(
        max_drawdown * 100,
        linestyle="--",
        linewidth=1,
        label=f"Max Drawdown: {max_drawdown:.3%}",
    )

    plt.title("Strategy Drawdown")
    plt.xlabel("Time")
    plt.ylabel("Drawdown (%)")
    plt.legend()
    plt.grid(True)

    plt.show()
