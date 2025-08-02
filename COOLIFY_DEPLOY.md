# 🚀 Instruções para Deploy no Coolify

## 📋 **Pré-requisitos**

### **1. Variáveis de Ambiente Necessárias:**

```bash
# Configurações do Banco de Dados
DB_HOST=pma.linksystems.com.br
DB_USER=adseg
DB_PASSWORD=Define@4536#8521
DB_NAME=litoral
DB_CHARSET=utf8mb4

# Credenciais de Login (para relatorio_v2_vps.py)
LOGIN_EMAIL=seu_email@exemplo.com
LOGIN_PASSWORD=sua_senha

# Configurações de Paths (Docker)
DOWNLOAD_PATH=/app/downloads
WKHTMLTOPDF_PATH=/usr/local/bin/wkhtmltopdf

# Webhook Secret (opcional)
WEBHOOK_SECRET=seu_secret_aqui
```

### **2. Portas Necessárias:**
- **8010:** Dashboard
- **8011:** Webhook Server

## 🔧 **Configuração no Coolify**

### **1. Criar Aplicação Dashboard:**

```yaml
# Nome da Aplicação
Dashboard-RelatorioWhats

# Build Pack
Dockerfile

# Porta
8010

# Comando de Inicialização
uvicorn main:app --host 0.0.0.0 --port 8010

# Variáveis de Ambiente
DB_HOST=pma.linksystems.com.br
DB_USER=adseg
DB_PASSWORD=Define@4536#8521
DB_NAME=litoral
DB_CHARSET=utf8mb4
LOGIN_EMAIL=seu_email@exemplo.com
LOGIN_PASSWORD=sua_senha
DOWNLOAD_PATH=/app/downloads
WKHTMLTOPDF_PATH=/usr/local/bin/wkhtmltopdf
```

### **2. Criar Aplicação Webhook:**

```yaml
# Nome da Aplicação
Webhook-RelatorioWhats

# Build Pack
Dockerfile

# Porta
8011

# Comando de Inicialização
uvicorn webhook_server:app --host 0.0.0.0 --port 8011

# Variáveis de Ambiente
DB_HOST=pma.linksystems.com.br
DB_USER=adseg
DB_PASSWORD=Define@4536#8521
DB_NAME=litoral
DB_CHARSET=utf8mb4
LOGIN_EMAIL=seu_email@exemplo.com
LOGIN_PASSWORD=sua_senha
DOWNLOAD_PATH=/app/downloads
WKHTMLTOPDF_PATH=/usr/local/bin/wkhtmltopdf
WEBHOOK_SECRET=seu_secret_aqui
```

## 📁 **Volumes Necessários**

### **Para ambas as aplicações:**
- **Downloads:** `/app/downloads` → `./downloads`
- **Logs:** `/app/logs` → `./logs`

## 🔗 **URLs Finais**

### **Dashboard:**
```
http://seu-servidor-coolify:8010
```

### **Webhook:**
```
http://seu-servidor-coolify:8011/webhook
```

## 📝 **Logs Importantes**

### **Dashboard Logs:**
- Verificar conexão com banco de dados
- Verificar carregamento de arquivos estáticos
- Verificar geração de PDFs

### **Webhook Logs:**
- Verificar recebimento de webhooks
- Verificar execução do `relatorio_v2_vps.py`
- Verificar geração de PDFs

## 🎯 **Teste Pós-Deploy**

### **1. Testar Dashboard:**
```bash
curl http://seu-servidor-coolify:8010
```

### **2. Testar Webhook:**
```bash
curl -X POST http://seu-servidor-coolify:8011/webhook \
  -H "Content-Type: application/json" \
  -d '{"edicao": 6409, "source_app": "teste"}'
```

### **3. Verificar PDFs:**
```bash
ls /app/downloads/
```

## ⚠️ **Observações Importantes**

1. **Credenciais:** Nunca commitar credenciais no Git
2. **Portas:** Usar 8010 e 8011 (não 8001)
3. **Volumes:** Compartilhar pasta downloads entre containers
4. **Logs:** Monitorar logs para identificar problemas
5. **Webhook:** Atualizar URL no script externo após deploy

## 🔄 **Atualização do Script Externo**

Após o deploy, atualizar o script externo com a nova URL:

```python
# Antes (local)
url = "http://localhost:8011/webhook"

# Depois (Coolify)
url = "http://seu-servidor-coolify:8011/webhook"
``` 