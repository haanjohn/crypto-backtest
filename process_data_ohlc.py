import pandas as pd
import argparse
import json

def process_data(coin):
    input_file = f"{coin}_historical_ohlc.json"
    output_file = f"{coin}_processed_ohlc.csv"

    # Load JSON manually
    with open(input_file, "r") as f:
        raw_data = json.load(f)  # Read list of lists format

    # Convert into DataFrame
    df = pd.DataFrame(raw_data, columns=["timestamp", "Open", "High", "Low", "Close"])

    # Convert timestamps from milliseconds to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Ensure no missing values
    df = df.dropna()

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Processed {coin} data with OHLC saved to {output_file}")

# Argument Parser for CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("coin", type=str, help="Coin name (e.g., bitcoin, ethereum)")
    args = parser.parse_args()

    process_data(args.coin)
