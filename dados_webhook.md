# 📡 Documentação do Webhook Server

## 🎯 **Objetivo**
Este webhook server recebe notificações de scripts externos quando uma rifa atinge 100% de andamento, gerando automaticamente o relatório PDF correspondente.

## 🔗 **Endpoint do Webhook**

### **URL Base (Local):**
```
http://localhost:8011/webhook
```

### **URL Base (Docker/Coolify):**
```
http://seu-servidor-coolify:8011/webhook
```

### **Método:**
```
POST
```

### **Headers:**
```
Content-Type: application/json
```

## 📋 **Formato da Solicitação**

### **Estrutura JSON:**
```json
{
    "edicao": 6409,
    "source_app": "nome_do_script_externo"
}
```

### **Campos Obrigatórios:**
- `edicao` (integer): Número da edição que atingiu 100%
- `source_app` (string): Nome do script que está enviando a notificação

### **Exemplo de Solicitação:**
```json
{
    "edicao": 6409,
    "source_app": "monitor_rifas"
}
```

## 🚀 **Como Implementar no Script Externo**

### **1. Detecção de 100%:**
Quando seu script detectar que uma rifa atingiu 100%:

```python
# Exemplo em Python
if rifa.andamento == "100%":
    enviar_webhook(rifa.edicao)

def enviar_webhook(edicao):
    import requests
    
    url = "http://localhost:8011/webhook"
    dados = {
        "edicao": edicao,
        "source_app": "meu_script_monitor"
    }
    
    response = requests.post(url, json=dados)
    print(f"Webhook enviado para edição {edicao}: {response.status_code}")
```

### **2. Exemplo em PowerShell:**
```powershell
# Quando detectar 100%
$edicao = 6409
$url = "http://localhost:8011/webhook"
$dados = @{
    edicao = $edicao
    source_app = "monitor_rifas"
} | ConvertTo-Json

Invoke-RestMethod -Uri $url -Method POST -Body $dados -ContentType "application/json"
```

### **3. Exemplo em cURL:**
```bash
# Quando detectar 100%
curl -X POST http://localhost:8011/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "edicao": 6409,
    "source_app": "monitor_rifas"
  }'
```

## ✅ **Resposta de Sucesso**

### **Status: 200 OK**
```json
{
    "success": true,
    "message": "Relatório gerado com sucesso para edição 6409",
    "pdf_path": "C:\\Users\\Adilson\\PycharmProjects\\LitoralAutomacoes\\Dashboard\\downloads\\relatorio-vendas-corujinha-rj-edicao-6409.pdf",
    "edition_info": {
        "sigla_oficial": "CORUJINHA",
        "data_formatada": "01/08/25"
    }
}
```

## ❌ **Resposta de Erro**

### **Status: 400 Bad Request**
```json
{
    "success": false,
    "error": "Edição 6409 não encontrada no sistema."
}
```

### **Status: 500 Internal Server Error**
```json
{
    "success": false,
    "error": "Erro interno do servidor"
}
```

## 🔄 **Fluxo Completo**

### **1. Script Externo Detecta 100%:**
```python
# Seu script monitorando as rifas
if rifa.andamento_percentual == "100%":
    print(f"🎯 Rifa {rifa.edicao} atingiu 100%!")
    enviar_webhook(rifa.edicao)
```

### **2. Envia Webhook:**
```python
def enviar_webhook(edicao):
    url = "http://localhost:8011/webhook"
    dados = {
        "edicao": edicao,
        "source_app": "meu_monitor"
    }
    
    try:
        response = requests.post(url, json=dados)
        if response.status_code == 200:
            print(f"✅ Webhook enviado com sucesso para edição {edicao}")
        else:
            print(f"❌ Erro ao enviar webhook: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
```

### **3. Webhook Server Processa:**
- Recebe a solicitação
- Valida a edição no banco de dados
- Chama `relatorio_v2_vps.py`
- Gera PDF na pasta `downloads/`
- Retorna confirmação

### **4. Dashboard Atualiza:**
- Verifica se PDF existe na pasta `downloads/`
- Exibe ícone de download quando disponível

## 📋 **Validações do Webhook Server**

### **1. Validação de Dados:**
- ✅ `edicao` é um número válido
- ✅ `source_app` é uma string válida
- ✅ Edição existe no banco de dados
- ✅ Edição não foi processada anteriormente

### **2. Validação de Processamento:**
- ✅ Edição está com status "concluído" (100%)
- ✅ Data de sorteio já passou
- ✅ PDF ainda não foi gerado

## 🔧 **Configurações do Webhook Server**

### **Porta (Local):**
```
8011
```

### **URL Completa (Local):**
```
http://localhost:8011/webhook
```

### **Porta (Docker/Coolify):**
```
8011
```

### **URL Completa (Docker/Coolify):**
```
http://seu-servidor-coolify:8011/webhook
```

### **Timeout:**
```
30 segundos para processamento
```

## 📝 **Logs do Webhook Server**

### **Logs de Sucesso:**
```
2025-08-02 00:13:50,713 - INFO - Solicitação recebida: {'edicao': 6409, 'source_app': 'monitor_rifas'}
2025-08-02 00:13:50,788 - INFO - Edição 6409 encontrada: CORUJINHA - 01/08/25
2025-08-02 00:13:50,797 - INFO - Gerando relatório edição 6409 - CORUJINHA - 01/08/25
2025-08-02 00:14:21,748 - INFO - PDF gerado com sucesso: C:\...\relatorio-vendas-corujinha-rj-edicao-6409.pdf
```

### **Logs de Erro:**
```
2025-08-02 00:13:50,713 - ERROR - Edição 6409 não encontrada no sistema.
2025-08-02 00:13:50,713 - ERROR - Edição 6409 já foi processada anteriormente.
```

## 🎯 **Resumo para Implementação**

### **No seu script externo:**

1. **Monitorar rifas** continuamente
2. **Detectar quando `andamento == "100%"`**
3. **Enviar webhook** para `http://localhost:8011/webhook`
4. **Aguardar resposta** para confirmar processamento
5. **Logar resultado** para auditoria

### **Exemplo Prático:**
```python
import requests
import time

def monitorar_rifas():
    while True:
        # Seu código de monitoramento aqui
        for rifa in rifas_ativas:
            if rifa.andamento == "100%":
                enviar_webhook(rifa.edicao)
        
        time.sleep(30)  # Verificar a cada 30 segundos

def enviar_webhook(edicao):
    url = "http://localhost:8011/webhook"
    dados = {
        "edicao": edicao,
        "source_app": "meu_monitor_rifas"
    }
    
    try:
        response = requests.post(url, json=dados, timeout=60)
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ PDF gerado: {resultado['pdf_path']}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

# Iniciar monitoramento
monitorar_rifas()
```

**Agora seu script externo sabe exatamente como notificar o webhook server quando uma rifa atingir 100%!** 🎉 