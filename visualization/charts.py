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
