import sys
import os

# Tambahkan path scripts agar bisa import modul
sys.path.insert(0, "/app/scripts")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


# ─── Task Functions ───────────────────────────────────────────────────────────

def task_extract(**context):
    from extract import extract
    df = extract()
    context["ti"].xcom_push(key="raw_data", value=df.to_json())
    print(f"[extract] Selesai, {len(df)} baris data.")


def task_transform(**context):
    import pandas as pd
    from transform import transform
    raw_json = context["ti"].xcom_pull(key="raw_data", task_ids="extract")
    df = pd.read_json(raw_json)
    df_ready = transform(df)
    context["ti"].xcom_push(key="transformed_data", value=df_ready.to_json())
    print(f"[transform] Selesai, {len(df_ready)} baris data siap.")


def task_train(**context):
    import pandas as pd
    import joblib
    from train import train_model

    transformed_json = context["ti"].xcom_pull(key="transformed_data", task_ids="transform")
    df_ready = pd.read_json(transformed_json)

    train_size = int(len(df_ready) * 0.8)
    train = df_ready[:train_size]

    X_train = train[["lag1", "lag2", "lag3"]]
    y_train = train["price"]

    model = train_model(X_train, y_train)

    os.makedirs("/app/scripts/artifacts", exist_ok=True)
    joblib.dump(model, "/app/scripts/artifacts/model.pkl")
    print("[train] Model selesai ditraining dan disimpan sementara.")


def task_forecast(**context):
    import pandas as pd
    import joblib
    from forecast import forecast_7days

    transformed_json = context["ti"].xcom_pull(key="transformed_data", task_ids="transform")
    df_ready = pd.read_json(transformed_json)

    model = joblib.load("/app/scripts/artifacts/model.pkl")
    forecast_df = forecast_7days(model, df_ready)

    context["ti"].xcom_push(key="forecast_data", value=forecast_df.to_json())
    print(f"[forecast] Forecast 7 hari selesai.")


def task_evaluate(**context):
    import pandas as pd
    from evaluate import evaluate_rmse

    transformed_json = context["ti"].xcom_pull(key="transformed_data", task_ids="transform")
    forecast_json = context["ti"].xcom_pull(key="forecast_data", task_ids="forecast")

    df_ready = pd.read_json(transformed_json)
    forecast_df = pd.read_json(forecast_json)

    train_size = int(len(df_ready) * 0.8)
    test = df_ready[train_size:]
    y_test = test["price"]

    if len(y_test) >= 7:
        rmse = evaluate_rmse(y_test.values[:7], forecast_df["forecast"].values)
    else:
        rmse = None
        print("[evaluate] Data test kurang dari 7, RMSE tidak dihitung.")

    context["ti"].xcom_push(key="rmse", value=rmse)
    print(f"[evaluate] RMSE: {rmse}")


def task_load(**context):
    import pandas as pd
    import joblib
    from load import save_model, save_metrics, save_forecast

    forecast_json = context["ti"].xcom_pull(key="forecast_data", task_ids="forecast")
    rmse = context["ti"].xcom_pull(key="rmse", task_ids="evaluate")

    forecast_df = pd.read_json(forecast_json)
    model = joblib.load("/app/scripts/artifacts/model.pkl")

    save_model(model)
    save_forecast(forecast_df)
    save_metrics({"RMSE": rmse})
    print("[load] Semua artifact berhasil disimpan!")


# ─── DAG Definition ───────────────────────────────────────────────────────────

with DAG(
    dag_id="crypto_forecast_7days",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["crypto", "forecast", "bitcoin"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=task_extract,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=task_transform,
    )

    train_task = PythonOperator(
        task_id="train",
        python_callable=task_train,
    )

    forecast_task = PythonOperator(
        task_id="forecast",
        python_callable=task_forecast,
    )

    evaluate_task = PythonOperator(
        task_id="evaluate",
        python_callable=task_evaluate,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=task_load,
    )

    # ─── Task Dependencies ────────────────────────────────────────────────────
    extract_task >> transform_task >> train_task >> forecast_task >> evaluate_task >> load_task