FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY .env.example .env
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
