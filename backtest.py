import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Moving Average Crossover Strategy
def moving_average_crossover_strategy(df, short_window=10, long_window=50, initial_cash=10000):
    df["short_ma"] = df["close"].rolling(window=short_window).mean()
    df["long_ma"] = df["close"].rolling(window=long_window).mean()
    df.dropna(inplace=True)

    cash = initial_cash
    holdings = 0
    trades = []
    portfolio_values = [initial_cash]  # Ensure the list starts correctly

    for i in range(len(df)):
        if i > 0 and holdings == 0 and df["short_ma"].iloc[i] > df["long_ma"].iloc[i] and df["short_ma"].iloc[i - 1] <= df["long_ma"].iloc[i - 1]:
            holdings = cash / df["close"].iloc[i]
            cash = 0
            trades.append((df.index[i], "BUY", df["close"].iloc[i], holdings))
        elif i > 0 and holdings > 0 and df["short_ma"].iloc[i] < df["long_ma"].iloc[i] and df["short_ma"].iloc[i - 1] >= df["long_ma"].iloc[i - 1]:
            cash = holdings * df["close"].iloc[i]
            holdings = 0
            trades.append((df.index[i], "SELL", df["close"].iloc[i], cash))
        portfolio_values.append(cash + (holdings * df["close"].iloc[i]))

    # Ensure portfolio_values matches the length of df.index
    while len(portfolio_values) < len(df):
        portfolio_values.append(portfolio_values[-1])
    
    if len(portfolio_values) > len(df):  # Trim extra if necessary
        portfolio_values = portfolio_values[:len(df)]

    final_value = cash + (holdings * df["close"].iloc[-1])
    return final_value, trades, portfolio_values


# Buy & Hold Strategy
def buy_and_hold_strategy(df, initial_cash=10000):
    holdings = initial_cash / df["close"].iloc[0]
    final_value = holdings * df["close"].iloc[-1]
    return final_value

# ATR Strategy
def atr_trading_strategy(df, atr_multiplier=2, initial_cash=10000):
    df.dropna(inplace=True)
    cash = initial_cash
    holdings = 0
    trades = []
    portfolio_values = []

    for i in range(len(df)):
        if i > 0 and df["ATR"].iloc[i] > atr_multiplier * df["ATR"].iloc[i-1]:
            if cash > 0:
                holdings = cash / df["close"].iloc[i]
                cash = 0
                trades.append((df.index[i], "BUY", df["close"].iloc[i], holdings))
        elif i > 0 and holdings > 0 and df["ATR"].iloc[i] < df["ATR"].iloc[i-1] * (atr_multiplier / 2):
            cash = holdings * df["close"].iloc[i]
            holdings = 0
            trades.append((df.index[i], "SELL", df["close"].iloc[i], cash))
        portfolio_values.append(cash + (holdings * df["close"].iloc[i]))

    final_value = cash + (holdings * df["close"].iloc[-1])
    return final_value, trades, portfolio_values

# Visualization function
def plot_results(df, trades, strategy_name, coin, portfolio_values, buy_hold_value, short_window=None, long_window=None, atr_multiplier=None):
    output_dir = "backtest_results"
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    ax1.plot(df.index, df["close"], label="Price", color="blue")
    for trade in trades:
        date, action, price, _ = trade
        color = "green" if action == "BUY" else "red"
        ax1.scatter(date, price, color=color, marker="^" if action == "BUY" else "v", s=100, label=action if action not in ax1.get_legend_handles_labels()[1] else "")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price")
    ax1.legend()

    if strategy_name == "Moving Average Crossover":
        param_str = f"[{short_window} - {long_window}]" 
    elif strategy_name == "ATR Strategy":
        param_str = f"[{atr_multiplier} multiplier]"
    ax1.set_title(f"{coin.upper()} - {strategy_name} {param_str} Backtest")

    ax2 = ax1.twinx()
    ax2.plot(df.index, portfolio_values, label="Portfolio Value", color="purple", linestyle="dotted")
    ax2.set_ylabel("Portfolio Value")
    ax2.legend(loc="upper left")

    plt.savefig(f"{output_dir}/{coin} - {strategy_name} {param_str}_backtest.png")
    plt.close()

    # Second Chart for Indicators
    plt.figure(figsize=(12, 6))
    if strategy_name == "Moving Average Crossover":
        plt.plot(df.index, df["short_ma"], label=f"Short MA", linestyle="dashed", color="orange")
        plt.plot(df.index, df["long_ma"], label=f"Long MA", linestyle="dashed", color="purple")
    elif strategy_name == "ATR Strategy":
        plt.plot(df.index, df["ATR"], label=f"ATR", linestyle="dashed", color="cyan")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Indicator Value")
    plt.title(f"{coin.upper()} - {strategy_name} Indicators {param_str}")
    plt.savefig(f"{output_dir}/{coin} - {strategy_name} {param_str}_indicators.png")
    plt.close()


# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("coin", type=str, help="Coin to analyze")
parser.add_argument("--strategy", type=str, choices=["ma-crossover", "atr"], required=True, help="Backtesting strategy")
parser.add_argument("--short", type=int, default=10, help="Short moving average window")
parser.add_argument("--long", type=int, default=50, help="Long moving average window")
parser.add_argument("--atr-multiplier", type=float, default=2, help="ATR multiplier for trading signals")
args = parser.parse_args()

# Load data
df = pd.read_csv(f"{args.coin}_processed.csv", parse_dates=["timestamp"], index_col="timestamp")

# Run backtest
if args.strategy == "ma-crossover":
    final_value, trades, portfolio_values = moving_average_crossover_strategy(df, args.short, args.long)
    strategy_name = "Moving Average Crossover"
elif args.strategy == "atr":
    final_value, trades, portfolio_values = atr_trading_strategy(df, args.atr_multiplier)
    strategy_name = "ATR Strategy"

buy_hold_value = buy_and_hold_strategy(df)

# Plot results
plot_results(df, trades, strategy_name, args.coin, portfolio_values, buy_hold_value, args.short, args.long, args.atr_multiplier)

print(f"✅ Final Portfolio Value ({strategy_name}): ${final_value:.2f}")
print(f"📈 Final Portfolio Value (Buy & Hold): ${buy_hold_value:.2f}")
if trades:
    for trade in trades:
        print(trade)

if final_value > buy_hold_value:
    print("🎉 Strategy outperformed Buy & Hold ✅")
else:
    print("📉 Strategy underperformed Buy & Hold ❌")
