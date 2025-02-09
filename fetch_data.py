import requests
import json
import sys
import os

# Constants
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

def fetch_historical_data(coin, days=365, currency="usd"):
    """
    Fetch historical market data from CoinGecko API.

    :param coin: Cryptocurrency name (e.g., "bitcoin", "ethereum").
    :param days: Number of days of historical data to fetch.
    :param currency: Quote currency (default: USD).
    """
    url = COINGECKO_API_URL.format(coin=coin)
    params = {"vs_currency": currency, "days": days, "interval": "daily"}
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json().get("prices", [])
        filename = f"{coin}_historical.json"
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        
        print(f"✅ Data saved to {filename}")
    else:
        print(f"❌ Failed to fetch data: {response.status_code}, {response.text}")

# Run script with arguments
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_data.py <coin_name> [days]")
        sys.exit(1)

    coin_name = sys.argv[1].lower()
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 365  # Default to 1 year

    fetch_historical_data(coin_name, days)
