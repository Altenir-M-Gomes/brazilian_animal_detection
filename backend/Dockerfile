# Usar imagem base leve com Python
FROM python:3.12-slim

# Configurações básicas
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Diretório da aplicação
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar lista de dependências
COPY requirements.txt .
COPY .env.example .env

# Atualizar pip e instalar pacotes
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Porta padrão
EXPOSE 8000

# Rodar FastAPI com Uvicorn (ajuste o módulo "app.main:app" conforme seu projeto)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
