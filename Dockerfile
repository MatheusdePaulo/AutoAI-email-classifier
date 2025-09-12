# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de requisitos primeiro (para aproveitar cache do Docker)
COPY requirements.txt .

# Instalar dependências do Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# Copiar o restante da aplicação
COPY . .

# Expor a porta que a aplicação vai rodar
EXPOSE 8000

# Comando para rodar a aplicação com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "120", "app:app"]