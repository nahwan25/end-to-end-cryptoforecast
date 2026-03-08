# 🪙 Crypto Forecast Pipeline

End-to-end MLOps pipeline untuk memprediksi harga Bitcoin 7 hari ke depan menggunakan Apache Airflow, scikit-learn, DVC, dan Docker.

---

## 📌 Deskripsi Project

Project ini membangun pipeline machine learning otomatis yang:
- Mengambil data harga Bitcoin dari CoinGecko API setiap hari
- Melakukan feature engineering (lag features)
- Melatih model MLP Regressor
- Memprediksi harga 7 hari ke depan
- Menyimpan model, forecast, dan metrik evaluasi

---

## 🏗️ Arsitektur Pipeline

```
CoinGecko API
      ↓
   extract          → Ambil data harga BTC 90 hari terakhir
      ↓
  transform         → Buat lag features (lag1, lag2, lag3)
      ↓
    train           → Training MLP Regressor (80% data)
      ↓
   forecast         → Prediksi harga 7 hari ke depan
      ↓
   evaluate         → Hitung RMSE
      ↓
     load           → Simpan model, forecast, dan metrik
```

---

## 🗂️ Struktur Folder

```
crypto-forecast-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
├── dags/
│   └── crypto_forecast_dag.py  # Airflow DAG
├── scripts/
│   ├── extract.py              # Ambil data dari CoinGecko API
│   ├── transform.py            # Feature engineering
│   ├── train.py                # Training model
│   ├── forecast.py             # Forecast 7 hari
│   ├── evaluate.py             # Evaluasi RMSE
│   └── load.py                 # Simpan artifacts
├── artifacts/                  # Output model & hasil (auto-generated)
│   ├── model.pkl
│   ├── forecast_7days.csv
│   └── metrics.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Tools | Kegunaan |
|-------|----------|
| Apache Airflow 2.7.1 | Workflow orchestration |
| scikit-learn | Machine learning (MLP Regressor) |
| pandas & numpy | Data processing |
| CoinGecko API | Sumber data harga Bitcoin |
| Docker & Docker Compose | Containerization |
| DVC | Data version control |
| GitHub Actions | CI/CD pipeline |
| PostgreSQL | Airflow metadata database |

---

## 🚀 Cara Menjalankan

### Prerequisites
- Docker Desktop sudah terinstall
- Python 3.11+
- Git

### 1. Clone repository
```bash
git clone https://github.com/USERNAME/crypto-forecast-pipeline.git
cd crypto-forecast-pipeline
```

### 2. Jalankan Docker
```bash
docker compose up --build
```

### 3. Buka Airflow UI
```
http://localhost:8082
```
Login dengan:
- Username: `admin`
- Password: cek di terminal (muncul saat pertama kali jalan)

### 4. Trigger DAG
- Aktifkan DAG `crypto_forecast_7days`
- Klik tombol ▶ untuk jalankan manual

### 5. Cek hasil
```bash
docker exec -it endtoend-airflow-1 cat /app/scripts/artifacts/metrics.json
docker exec -it endtoend-airflow-1 cat /app/scripts/artifacts/forecast_7days.csv
```

---

## ⚙️ Konfigurasi

### Environment Variables (`docker-compose.yml`)
| Variable | Nilai |
|----------|-------|
| `AIRFLOW__CORE__EXECUTOR` | LocalExecutor |
| `AIRFLOW__CORE__FERNET_KEY` | (generate sendiri) |
| `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` | postgresql+psycopg2://airflow:airflow@postgres/airflow |

### Generate Fernet Key
```bash
docker run --rm apache/airflow:2.7.1-python3.11 python -c \
  "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## 📊 Model

- **Algoritma:** MLP Regressor (Multi-Layer Perceptron)
- **Features:** lag1, lag2, lag3 (harga 1, 2, 3 hari sebelumnya)
- **Target:** Harga Bitcoin (USD)
- **Split:** 80% train / 20% test
- **Evaluasi:** RMSE (Root Mean Square Error)
- **Hidden Layers:** (64, 32)
- **Max Iterations:** 500

---

## 🔄 CI/CD

Setiap push ke branch `main` akan otomatis trigger GitHub Actions untuk build Docker image dan memastikan tidak ada error.

```
Push ke main → GitHub Actions → Build Docker Image → ✅ / ❌
```

---

## 📦 Data Versioning

Project ini menggunakan DVC untuk tracking data:

```bash
# Pull data terbaru
dvc pull

# Setelah DAG jalan, update data
dvc add scripts/data/raw/crypto_price.csv
dvc push
git add scripts/data/raw/crypto_price.csv.dvc
git commit -m "update data"
git push
```

---

## 📝 DAG Schedule

| Parameter | Nilai |
|-----------|-------|
| Schedule | `@daily` (setiap hari) |
| Start Date | 2024-01-01 |
| Catchup | False |
| Tags | crypto, forecast, bitcoin |
