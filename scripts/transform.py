import pandas as pd

def transform(df):
    """
    Buat lag features dari kolom price.
    """
    df = df.copy()
    df["lag1"] = df["price"].shift(1)
    df["lag2"] = df["price"].shift(2)
    df["lag3"] = df["price"].shift(3)
    df = df.dropna().reset_index(drop=True)
    print(f"[transform] Data setelah transform: {len(df)} baris.")
    return df