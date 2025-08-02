FROM python:3.12-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome (versão corrigida)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar ChromeDriver (versão dinâmica - detecta automaticamente) - COM VERIFICAÇÃO DE CONTEÚDO
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F'.' '{print $1}') \
    && echo "Chrome version detected: $CHROME_VERSION" \
    && wget --no-verbose "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION.0.7204.183/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip \
    && ls -la /tmp/chromedriver.zip \
    && unzip -l /tmp/chromedriver.zip \
    && unzip -o /tmp/chromedriver.zip -d /tmp/ \
    && ls -la /tmp/ \
    && cp /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && chromedriver --version

# Instalar wkhtmltopdf (versão corrigida)
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xfonts-75dpi \
    xfonts-base \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements primeiro (cache)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código
COPY . .

# Criar diretórios necessários
RUN mkdir -p /app/logs /app/downloads /app/scripts/logs

# Expor portas
EXPOSE 8010 8011

# Comando de inicialização
CMD ["python", "main.py"] 