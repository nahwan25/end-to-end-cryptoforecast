import joblib
import json
import os

def save_model(model, path="scripts/artifacts/model.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"[load] Model disimpan ke {path}")

def save_metrics(metrics, path="scripts/artifacts/metrics.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[load] Metrics disimpan ke {path}: {metrics}")

def save_forecast(forecast_df, path="scripts/artifacts/forecast_7days.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    forecast_df.to_csv(path, index=False)
    print(f"[load] Forecast disimpan ke {path}")