import pandas as pd

def forecast_7days(model, df_latest):
    """
    Forecast harga 7 hari ke depan menggunakan lag features.
    df_latest: dataframe dengan kolom lag1, lag2, lag3
    """
    forecasts = []

    # Ambil nilai lag terakhir
    lag1 = df_latest["lag1"].iloc[-1]
    lag2 = df_latest["lag2"].iloc[-1]
    lag3 = df_latest["lag3"].iloc[-1]
    last_price = df_latest["price"].iloc[-1]

    # Sliding window manual
    window = [lag3, lag2, lag1, last_price]  # urutan dari terlama ke terbaru

    for i in range(7):
        X_pred = [[window[-3], window[-2], window[-1]]]
        pred = model.predict(X_pred)[0]
        forecasts.append(pred)
        window.append(pred)

    print(f"[forecast] Forecast 7 hari: {forecasts}")
    return pd.DataFrame({"forecast": forecasts})