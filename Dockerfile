# -----------------------------------------------------------------------------
# Dockerfile para a aplicação Flask 'AutoAI' (VERSÃO FINAL COM PERMISSÃO FORÇADA)
# -----------------------------------------------------------------------------

# Etapa 1: Definir a imagem base
FROM python:3.9-slim

# Etapa 2: Configurar o ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HF_HOME=/app/cache

# Define o diretório de trabalho
WORKDIR /app

# Etapa 3: Instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 4: Copiar o código da aplicação
COPY . .

# *** MUDANÇA IMPORTANTE ***
# Cria o diretório de cache manualmente e dá permissão total (leitura/escrita/execução)
# para garantir que não haja nenhum conflito de permissão.
RUN mkdir -p /app/cache && chmod -R 777 /app/cache

# Etapa 5: Expor a porta
EXPOSE 8000

# Etapa 6: Definir o comando de execução
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "app:app"]