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

# Instalar Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
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