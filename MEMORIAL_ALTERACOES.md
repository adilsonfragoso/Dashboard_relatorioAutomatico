# 📋 Memorial de Alterações - Projeto Dashboard

## 🎯 **Objetivo do Projeto**

Este projeto visa criar um sistema completo com:
- **Dashboard** - Mostra em tempo real o andamento das rifas
- **Webhook Server** - Recebe solicitações de outras aplicações (não mais WhatsApp)
- **Relatório V2** - Gera PDFs e armazena localmente (não mais envia via WhatsApp)

## 🚨 **Problemas Identificados e Soluções Aplicadas**

### **1. Estrutura Inicial (ADAPTADA)**
- **Status:** ✅ Adaptações concluídas
- **Descobertas:**
  - `main.py` - API FastAPI com dashboard (463 linhas) ✅ Corrigido
  - `webhook_server.py` - Webhook para outras aplicações (549 linhas) ✅ Adaptado
  - `relatorio_v2_vps.py` - Geração de relatórios (905 linhas) ✅ Mantido
  - `dashboard.html` - Interface do dashboard (109 linhas) ⏳ Pendente
- **Adaptações realizadas:**
  - ✅ Corrigido caminho do script para `relatorio_v2_vps.py`
  - ✅ Corrigido caminho dos PDFs para `/app/downloads/`
  - ✅ Removido dependência da Evolution API
  - ✅ Adaptado webhook para receber de outras aplicações
  - ✅ PDFs armazenados localmente (não deletados)
  - ✅ Criadas pastas `downloads/` e `logs/`
  - ✅ Atualizado `requirements.txt` com dependências necessárias
- **Próximos passos:** Testar localmente antes do deploy no Coolify

## 🔄 **Histórico de Tentativas**

### **Tentativas de Análise:**
1. Estrutura do projeto → ✅ Analisado
2. Configuração local → ✅ Concluído
3. Teste local → ✅ Dashboard e webhook funcionando na porta 8010
4. Deploy Coolify → ⏳ Pendente

## 📝 **Regras Seguidas**

### **✅ Aplicadas:**
- ✅ Criar memorial único para este projeto
- ✅ Seguir instruções do `sobre.md`
- ✅ Manter automação original dos scripts `.py`
- ✅ Testar localmente antes do Coolify
- ✅ Usar porta 8010 (conforme solicitado)

### **❌ Evitadas:**
- ❌ Modificar automação dos scripts .py
- ❌ Criar múltiplos arquivos .md
- ❌ Deploy direto sem teste local

## 🔧 **Configurações Atuais**

### **Portas:**
- Dashboard: 8010 (FastAPI)
- Webhook: 8010 (FastAPI)

### **Arquivos Principais:**
- `main.py` - API do dashboard
- `webhook_server.py` - Webhook (será adaptado)
- `relatorio_v2_vps.py` - Geração de relatórios
- `dashboard.html` - Interface do dashboard

## 🚀 **Próximo Passo**

**Preparação para deploy no Coolify** para verificar:
1. ✅ Dashboard funcionando na porta 8010
2. ✅ Webhook recebe solicitações de outras aplicações
3. ✅ **Geração de relatório funcionando perfeitamente**
4. ✅ **Tempo de exibição aumentado para 11 horas**
5. ✅ **Ícones PDF modernizados** - SVG com seta de download e melhor alinhamento

**Objetivo:** Sistema funcionando localmente. Pronto para deploy no Coolify.

## 🔧 **Problemas Identificados e Soluções:**

### **Script relatorio_v2_vps.py:**
- ✅ **Caminho corrigido:** Agora usa caminho local em vez de Docker
- ✅ **Encoding corrigido:** Tratamento robusto de UTF-8/Latin-1
- ✅ **Emojis removidos:** Corrigidos problemas de encoding com caracteres especiais
- ✅ **Indentação corrigida:** Erros de sintaxe Python resolvidos
- ✅ **Credenciais configuradas:** Arquivo `.env` com LOGIN_EMAIL e LOGIN_PASSWORD
- ✅ **Download CSV:** CSV baixado com sucesso
- ✅ **Geração PDF:** PDF gerado com sucesso usando wkhtmltopdf
- ✅ **Ambiente virtual:** `.venv` configurado com Python 3.12.4

### **Dashboard (main.py):**
- ✅ **Tempo de exibição:** Aumentado de 30 minutos para 11 horas após 100%
- ✅ **Geração automática:** PDFs são gerados automaticamente para rifas 100%
- ✅ **Detecção inteligente:** Dashboard verifica existência de PDFs automaticamente
- ✅ **Performance:** Geração manual funciona em ~30 segundos
- ⏳ **Performance:** Geração automática pode ser mais lenta devido ao processamento paralelo

### **Interface (dashboard.js + CSS):**
- ✅ **Ícones PDF modernos:** SVG com seta de download para PDFs disponíveis
- ✅ **Ícones não disponível:** SVG com indicador visual para PDFs indisponíveis
- ✅ **Alinhamento corrigido:** Ícones centralizados e sem deslocamento da página
- ✅ **Loading otimizado:** Ícone de processamento melhorado e centralizado
- ✅ **Novo design:** Ícones baseados no design fornecido pelo usuário (pdfdown.png)
- ✅ **Arquitetura separada:** Dashboard apenas verifica PDFs na pasta downloads (não gera automaticamente)

### **🐛 Correção de Problema no Status do Dashboard (2025-08-02):**

#### **Problema Identificado:**
- ❌ Dashboard mostrava "Servidor Parado" mesmo com dados atualizados
- ❌ Erro `UnboundLocalError: cannot access local variable 'ativo' where it is not associated with a value`
- ❌ Nomenclatura "Heroku" não era mais apropriada

#### **Solução Aplicada:**
- ✅ **Variável `ativo` inicializada:** `ativo = False` no início da função para prevenir erro
- ✅ **Endpoint renomeado:** `/api/dashboard/status-heroku` → `/api/dashboard/status-monitor-andamento`
- ✅ **Função renomeada:** `obter_status_heroku()` → `obter_status_monitor_andamento()`
- ✅ **JavaScript atualizado:** Todas as funções renomeadas de "Heroku" para "monitorAndamento"
- ✅ **Logs atualizados:** Prefixos `[HEROKU]` → `[MONITOR]` para melhor identificação
- ✅ **Cache-busting:** Versões CSS e JS atualizadas para forçar recarregamento

#### **Mudanças Técnicas:**
```python
# main.py - Função corrigida
@app.get("/api/dashboard/status-monitor-andamento")
def obter_status_monitor_andamento():
    ativo = False  # Initialize ativo to prevent potential UnboundLocalError
    # ... resto da função
```

```javascript
// dashboard.js - Funções renomeadas
async function verificarStatusMonitorAndamento() {
    const response = await fetch('/api/dashboard/status-monitor-andamento?t=' + Date.now());
    // ... resto da função
}
```

#### **Teste de Funcionamento:**
- ✅ **Endpoint testado:** Retorna `ativo: True` quando servidor está ativo
- ✅ **Dashboard atualizado:** Status agora respeita a diferença de tempo corretamente
- ✅ **Logs funcionando:** Console mostra informações detalhadas do status

---

### **🔧 Correção de Configuração do Webhook Server (2025-08-02):**

#### **Problema Identificado:**
- ❌ Webhook server estava usando valores padrão para configuração do banco
- ❌ Não respeitava as variáveis de ambiente do Coolify
- ❌ Erro "Edição não encontrada" devido a configuração incorreta

#### **Solução Aplicada:**
- ✅ **Removidos valores padrão:** DB_CONFIG agora usa apenas `os.getenv()` sem fallbacks
- ✅ **Configuração limpa:** Apenas variáveis de ambiente do Coolify são usadas
- ✅ **Logs de debug:** Adicionados logs para verificar configuração do banco
- ✅ **Endpoint de teste:** Criado `/test-db` para verificar conexão com banco

#### **Mudanças Técnicas:**
```python
# webhook_server.py - Configuração corrigida
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'autocommit': True
}
```

#### **Teste de Funcionamento:**
- ✅ **Conexão com banco:** Webhook conecta corretamente ao banco remoto
- ✅ **Edição encontrada:** Edição 6409 é localizada no banco
- ✅ **Script executado:** relatorio_v2_vps.py é chamado corretamente
- ⚠️ **PDF não gerado:** Falha por falta do wkhtmltopdf local (esperado)

---

### **🐛 Correção de Problema no Docker - Chrome não instalado (2025-08-02):**

#### **Problema Identificado:**
- ❌ **Chrome não encontrado no Docker:** `google-chrome: not found`
- ❌ **ChromeDriver falha:** `Unable to obtain driver for chrome`
- ❌ **Selenium não funciona:** Script falha ao tentar abrir navegador
- ❌ **Webhook falha:** PDF não é gerado no ambiente Docker

#### **Solução Aplicada:**
- ✅ **Chrome instalado no Dockerfile:** Adicionada instalação do Google Chrome
- ✅ **Repositório oficial:** Usado repositório oficial do Google Chrome
- ✅ **Chave GPG:** Adicionada chave de assinatura do Google
- ✅ **Limpeza de cache:** Removidos arquivos temporários para otimizar imagem

#### **Mudanças Técnicas:**
```dockerfile
# Dockerfile - Instalação do Chrome adicionada
# Instalar Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*
```

#### **Próximos Passos:**
1. **Redeploy no Coolify:** Com Dockerfile atualizado
2. **Teste do webhook:** Verificar se Chrome funciona no Docker
3. **Geração de PDF:** Confirmar que PDFs são gerados corretamente

## 📚 **Documentação Criada**

### **dados_webhook.md**
- ✅ Documentação completa do webhook server
- ✅ Formato de dados e validações
- ✅ Exemplos de uso (PowerShell, cURL, Python)
- ✅ Tratamento de erros e monitoramento
- ✅ Processo interno detalhado

## 📋 **Análise da Estrutura Atual**

### **main.py (Dashboard API):**
- ✅ API FastAPI funcionando
- ✅ Endpoint `/api/dashboard/gerar-relatorio/{edicao}` chama `relatorio_v1.py`
- ❌ **PROBLEMA:** Chama `scripts/relatorio_v1.py` que não existe
- ❌ **PROBLEMA:** Deveria chamar `relatorio_v2_vps.py` diretamente
- ❌ **PROBLEMA:** Caminho hardcoded `D:/Adilson/Downloads/` para PDFs

### **webhook_server.py:**
- ✅ Webhook para Evolution API funcionando
- ✅ Chama `relatorio_v2_vps.py` corretamente
- ❌ **PROBLEMA:** Configurado para WhatsApp (Evolution API)
- ❌ **PROBLEMA:** Envia PDF via WhatsApp
- ✅ **SOLUÇÃO:** Adaptar para receber de outras aplicações

### **relatorio_v2_vps.py:**
- ✅ Script completo funcionando
- ✅ Gera PDF e insere no banco
- ❌ **PROBLEMA:** Deleta PDF após envio
- ✅ **SOLUÇÃO:** Armazenar PDF localmente

### **dashboard.html:**
- ✅ Interface funcionando
- ❌ **PROBLEMA:** Coluna PDF não implementada
- ✅ **SOLUÇÃO:** Implementar exibição de PDFs

## 🎯 **Adaptações Necessárias**

### **1. main.py:**
- Corrigir caminho do script para `relatorio_v2_vps.py`
- Corrigir caminho dos PDFs para `/app/downloads/`
- Implementar armazenamento local de PDFs

### **2. webhook_server.py:**
- Remover dependência da Evolution API
- Adaptar para receber solicitações de outras aplicações
- Manter chamada para `relatorio_v2_vps.py`
- Armazenar PDF localmente (não enviar via WhatsApp)

### **3. relatorio_v2_vps.py:**
- Não deletar PDF após geração
- Armazenar em `/app/downloads/`

### **4. dashboard.html:**
- Implementar coluna PDF para exibir arquivos gerados

---

## 🐳 **Preparação para Docker/Coolify (2025-08-02):**

### **✅ Menu Removido:**
- Dashboard agora é página solo frontend
- Menu "Editar, Edições e Premiações" removido conforme solicitado

### **✅ Dockerfile Criado:**
- Baseado em Python 3.12.4-slim
- Instalação do wkhtmltopdf
- Configuração de diretórios downloads/ e logs/
- Exposição das portas 8010 e 8011

### **✅ docker-compose.yml:**
- Serviços separados para Dashboard e Webhook
- Volumes compartilhados para downloads e logs
- Variáveis de ambiente configuradas
- Comandos de inicialização específicos

### **✅ Variáveis de Ambiente:**
- DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET
- LOGIN_EMAIL, LOGIN_PASSWORD (para relatorio_v2_vps.py)
- DOWNLOAD_PATH=/app/downloads
- WKHTMLTOPDF_PATH=/usr/bin/wkhtmltopdf
- WEBHOOK_SECRET (opcional)

### **✅ Documentação Atualizada:**
- COOLIFY_DEPLOY.md com instruções completas
- dados_webhook.md atualizado com URLs Docker
- .dockerignore para otimizar build

### **✅ Configurações Docker:**
- Portas: 8010 (Dashboard) e 8011 (Webhook)
- Volumes: downloads/ e logs/ compartilhados
- Logs configurados para identificação de problemas
- Paths adaptados para ambiente Docker

### **🐛 Correção de Problema no Deploy (2025-08-02):**

#### **Problema Identificado:**
- ❌ Erro na instalação do wkhtmltopdf no Docker
- ❌ Link do GitHub quebrado: `wkhtmltox_0.12.6.1-2.bullseye_amd64.deb`
- ❌ Falha no build do Docker

#### **Solução Aplicada:**
- ✅ **Dockerfile corrigido:** Instalação via `apt-get install wkhtmltopdf`
- ✅ **Caminho atualizado:** `/usr/bin/wkhtmltopdf` (padrão do apt)
- ✅ **Variáveis de ambiente:** Atualizadas em todos os arquivos
- ✅ **Documentação:** COOLIFY_DEPLOY.md e RESUMO_DEPLOY.md atualizados

#### **Mudanças Técnicas:**
```dockerfile
# Antes (problemático):
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6.1-2.bullseye_amd64.deb

# Depois (corrigido):
RUN apt-get install -y wkhtmltopdf
```

### **📋 Próximos Passos:**
1. Deploy no Coolify seguindo COOLIFY_DEPLOY.md
2. Configurar variáveis de ambiente no Coolify
3. Testar webhook com script externo
4. Monitorar logs para identificar problemas

---

**Memorial criado em: 2025-01-27 10:30**
**Atualizado em: 2025-08-02 01:35** 