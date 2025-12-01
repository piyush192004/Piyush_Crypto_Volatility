import requests
import pandas as pd

def fetch_crypto_data(coin, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "inr", "days": days}

    r = requests.get(url, params=params)
    data = r.json()

    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

coins = ["bitcoin", "ethereum", "solana", "dogecoin", "cardano"]

for c in coins:
    df = fetch_crypto_data(c)
    df.to_csv(f"data/{c}.csv")
