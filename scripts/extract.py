import requests
import pandas as pd
import os

def extract(path="scripts/data/raw/crypto_price.csv"):
    """
    Ambil data harga Bitcoin 90 hari terakhir dari CoinGecko API,
    lalu simpan ke CSV.
    """
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "90",
        "interval": "daily"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Parse data harga
    prices = data["prices"]  # list of [timestamp_ms, price]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.sort_values("date").reset_index(drop=True)

    # Simpan ke CSV
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"[extract] Data berhasil disimpan ke {path}, total {len(df)} baris.")

    return df