import pandas as pd
import argparse
import json

def process_data(coin):
    #Processes historical JSON data into a clean CSV format with ATR calculations.
    input_file = f"{coin}_historical.json"
    output_file = f"{coin}_processed.csv"

    # Load JSON manually
    with open(input_file, "r") as f:
        raw_data = json.load(f)  # Read list of lists format

    # Convert into DataFrame
    df = pd.DataFrame(raw_data, columns=["timestamp", "price"])
    
    # Convert timestamps from milliseconds to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Ensure no missing values
    df = df.dropna()

    # ATR Calculation (Fixing Any Issues)
    df["prev_close"] = df["price"].shift(1)
    df["high-low"] = df["price"].rolling(window=2).max() - df["price"].rolling(window=2).min()
    df["high-prev_close"] = (df["price"] - df["prev_close"]).abs()
    df["low-prev_close"] = (df["prev_close"] - df["price"]).abs()

    df["true_range"] = df[["high-low", "high-prev_close", "low-prev_close"]].max(axis=1)

    # Compute 14-day ATR (standard ATR period)
    df["ATR"] = df["true_range"].rolling(window=14).mean()

    # Ensure ATR column is filled
    df = df.dropna()
    df.rename(columns={"price": "close"}, inplace=True)


    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Processed {coin} data with ATR saved to {output_file}")

# Argument Parser for CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("coin", type=str, help="Coin name (e.g., bitcoin, ethereum)")
    args = parser.parse_args()

    process_data(args.coin)
