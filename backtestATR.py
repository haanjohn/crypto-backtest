import pandas as pd
import argparse
from backtesting import Backtest, Strategy

class ATRStrategy(Strategy):
    # Default strategy parameters (will be updated from command line)
    ema_short_period = 9
    ema_long_period = 21
    atr_period = 10

    def init(self):
        # Calculate the 9-day and 21-day exponential moving averages on the Close price.
        self.ema9 = self.I(lambda x: pd.Series(x).ewm(span=self.ema_short_period, adjust=False).mean(), self.data.Close)
        self.ema21 = self.I(lambda x: pd.Series(x).ewm(span=self.ema_long_period, adjust=False).mean(), self.data.Close)
        self.atr = self.I(
           lambda high, low: pd.Series(high - low).rolling(self.atr_period).mean(),
            self.data.High, self.data.Low
        )

        # Variables to store trade entry details (for setting dynamic targets)
        self.entry_price = None     # Price at which the current trade was entered.
        self.entry_atr = None       # ATR value at the time of entry.
        self.partial_taken = False  # Flag to indicate if the first profit target has been hit.

    def next(self):
        # If no position is open, check for a new entry.
        if not self.position:
            # Reset trade-specific variables if flat.
            self.entry_price = None
            self.entry_atr = None
            self.partial_taken = False

            # Check the long-entry condition: 9-day EMA > 21-day EMA.
            if self.ema9[-1] > self.ema21[-1]:
                self.buy()  # Enter long
        else:
            # A position is open.
            if self.entry_price is None and self.trades:
                # Record the entry price from the last trade executed.
                self.entry_price = self.trades[-1].entry_price
                self.entry_atr = self.atr[-1]

            # Define the target and stop levels based on the entry price and the ATR at entry.
            target_level = self.entry_price + 0.5 * self.entry_atr
            stop_level   = self.entry_price - 0.25 * self.entry_atr

            # Check for stop loss.
            if self.data.Low[-1] <= stop_level:
                self.position.close()  # Exit the entire position.
            # Check for the partial profit target.
            elif (not self.partial_taken) and (self.data.High[-1] >= target_level):
                # For a partial exit, we issue a sell order reducing our position by 50%.
                self.sell(size=self.position.size * 0.5)
                self.partial_taken = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Mandatory coin argument.
    parser.add_argument("coin", type=str, help="Coin name (e.g., bitcoin, ethereum)")
    # Optional arguments for strategy parameters.
    parser.add_argument("--ema_short", type=int, default=9, help="Short EMA period")
    parser.add_argument("--ema_long", type=int, default=21, help="Long EMA period")
    parser.add_argument("--atr", type=int, default=10, help="ATR period")
    args = parser.parse_args()

    # Dynamically update the ATRStrategy parameters based on the command-line input.
    ATRStrategy.ema_short_period = args.ema_short
    ATRStrategy.ema_long_period = args.ema_long
    ATRStrategy.atr_period = args.atr

    # Construct the file name for the historical data.
    file_name = f"{args.coin}_processed_ohlc.csv"
    data = pd.read_csv(file_name)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)

    # Initialize the backtest.
    bt = Backtest(data, ATRStrategy, cash=50000, commission=0.002)

    # Run the backtest and print statistics.
    stats = bt.run()
    print(stats)

    # Build a dynamic result filename using the strategy name, coin, and parameters.
    result_filename = f"ATRStrategy-{args.coin}-{args.ema_short}-{args.ema_long}-{args.atr}.html"
    
    # Plot the results and save them to the dynamically named HTML file.
    bt.plot(filename=result_filename)
