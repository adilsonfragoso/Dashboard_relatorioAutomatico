# Dockerfile para Dashboard e Webhook Server
FROM python:3.12.4-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    xvfb \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro para cache de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p downloads logs

# Expor portas
EXPOSE 8010 8011

# Comando padrão (será sobrescrito pelo Coolify)
CMD ["python", "main.py"] 