FROM apache/airflow:2.7.1-python3.11

# Set working dir
WORKDIR /app

# Install dependencies tambahan dari requirements.txt (opsional)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Default command
CMD ["airflow", "standalone"]