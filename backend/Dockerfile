# Use uma imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Copia os requisitos
COPY requirements.txt .

# Instala as dependências
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando para rodar a API
# Comando para rodar a API (usando $PORT do Render)
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
