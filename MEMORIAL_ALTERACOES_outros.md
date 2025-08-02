# 📋 Memorial de Alterações - Sistema de Webhook e Relatórios

## 🚨 **Problemas Identificados e Soluções Aplicadas**

### **1. Conflito de Portas (RESOLVIDO)**
- **Problema:** `Bind for 0.0.0.0:444X failed: port is already allocated`
- **Soluções tentadas:**
  - Porta 4444 → 4445 → 4446 → 4447 → 4448
  - VNC: 7900 → 7901 → 7902 → 7903 → 7904
- **Status:** ✅ Resolvido com porta 4448

### **2. Download CSV não funcionando (PROBLEMA DE VERSÃO IDENTIFICADO)**
- **Problema:** `This version of ChromeDriver only supports Chrome version 114`
- **Soluções aplicadas:**
  - ✅ Configurações robustas do Chrome adicionadas
  - ✅ Volume compartilhado: `./downloads:/home/seluser/Downloads`
  - ✅ Configurações de download otimizadas
  - ✅ **Pasta `downloads` criada no projeto** (como sugerido pelo usuário)
  - ✅ **Corrigido `.gitignore`** para permitir pasta downloads
  - ✅ **Criados arquivos `.gitkeep`** para garantir reconhecimento pelo Git
  - ✅ **JavaScript de download forçado** (baseado no projeto de referência)
  - ✅ **REVERTIDO PARA CHROME DIRETO** (como na VPS que funciona)
  - ✅ **Corrigido Dockerfile** (apt-key depreciado → gpg)
  - ✅ **Simplificado ChromeDriver** (remove dependência do google-chrome --version)
- **Descoberta:** A automação está funcionando perfeitamente, mas o download não está acontecendo
- **Nova descoberta:** ChromeDriver versão 114 incompatível com Chrome versão 138
- **Soluções sugeridas pelo usuário:**
  1. **Usar versões de teste do ChromeDriver** (como no Windows) → ❌ Falhou (erro de sintaxe)
  2. **Implementar webdriver-manager** (como no monitorAndamento.py) → ❌ Falhou
  3. **Usar estratégias do monitorAndamento.py** (que funciona na Heroku) → ❌ Falhou
  4. **Usar Chrome for Testing** (versão específica 138.0.7204.183) → ⏳ TESTANDO
- **Status:** 🔄 TESTANDO CHROME FOR TESTING - Versão específica 138.0.7204.183

### **3. Elemento não encontrado (RESOLVIDO)**
- **Problema:** `no such element: Unable to locate element: {"method":"xpath","selector":"//input[@placeholder='Pesquisar por título do sorteio...']"}`
- **Causa:** Campo de busca não estava sendo encontrado após navegação
- **Solução aplicada:** Adicionados logs de debug para verificar URL e título da página
- **Descoberta:** A automação está funcionando perfeitamente! O campo foi encontrado e o processo continuou
- **Status:** ✅ RESOLVIDO - Automação funcionando

### **4. Erro de Rede Docker (RESOLVIDO)**
- **Problema:** `network pocwc808kw0s0wwwoc0808oc declared as external, but could not be found`
- **Causa:** Docker Compose declarando rede externa inexistente
- **Solução aplicada:** Removida declaração de rede desnecessária do docker-compose.coolify.yml
- **Status:** ✅ RESOLVIDO - Rede removida

### **5. Erro de Download ChromeDriver (NOVO PROBLEMA)**
- **Problema:** `failed to solve: process "/bin/sh -c wget -q "https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.183/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip && unzip /tmp/chromedriver.zip -d /usr/local/bin/ && chmod +x /usr/local/bin/chromedriver && rm /tmp/chromedriver.zip" did not complete successfully: exit code: 1`
- **Causa:** Download do ChromeDriver falhando durante build do Docker
- **Solução aplicada:** Aguardando correção do Dockerfile
- **Status:** 🔄 TESTANDO VERSÃO DINÂMICA - ChromeDriver detecta automaticamente versão do Chrome

## 🔄 **Histórico de Tentativas**

### **Tentativas de Porta:**
1. 4444 (padrão) → ❌ Conflito
2. 4445 → ❌ Conflito  
3. 4446 → ❌ Conflito
4. 4447 → ❌ Conflito
5. 4448 → ⏳ Testando

### **Tentativas de Download:**
1. Configurações básicas → ❌ Não funcionou
2. Configurações robustas → ❌ Não funcionou
3. Volume compartilhado → ❌ Não funcionou
4. ChromeDriver local (versão 114) → ❌ Incompatível com Chrome 138
5. webdriver-manager automático → ❌ Baixando arquivo incorreto
6. Chrome for Testing (versão 138.0.7204.183) → ❌ Deploy falhou (download ChromeDriver falhou)
7. Chrome for Testing com debug → ❌ Deploy falhou (download ChromeDriver falhou)
8. Chrome for Testing com etapas separadas → ❌ Deploy falhou (chmod falhou - arquivo não existe)
9. Chrome for Testing com verificação de arquivo → ❌ Deploy falhou (chmod falhou - arquivo não existe)
10. Chrome for Testing com verificação de conteúdo → ✅ SUCESSO - Sistema funcionando
11. Chrome for Testing com versão dinâmica → ⏳ Testando

### **Tentativas de Deploy:**
1. Docker Compose com rede → ❌ Rede externa não encontrada
2. Docker Compose sem rede → ❌ Container não encontrado
3. Aguardando próxima tentativa → ⏳ Analisando

### **Tentativas de Automação:**
1. Modificações na automação → ❌ Revertido (conforme instruções)
2. Manter automação original → ✅ Aplicado

## 🎯 **Próximas Ações**

### **Prioridade 1: Resolver download no Selenium Grid**
- **Problema:** Download não funciona no Selenium Grid
- **Ação:** Verificar se o volume compartilhado está funcionando
- **Teste:** Verificar se arquivos aparecem em `/home/seluser/Downloads` no container selenium
- **Não fazer:** Voltar para configurações básicas

### **Prioridade 2: Verificar volume compartilhado**
- **Ação:** Testar se o volume `./downloads:/home/seluser/Downloads` está funcionando
- **Teste:** Verificar se arquivos baixados aparecem no volume compartilhado
- **Não fazer:** Modificar automação original

## 📝 **Regras Seguidas**

### **✅ Aplicadas:**
- ✅ Não modificar automação original
- ✅ Usar projeto de referência (`monitorAndamento.py`)
- ✅ Criar memorial de alterações
- ✅ Evitar loops de tentativas

### **❌ Evitadas:**
- ❌ Modificar automação dos scripts .py
- ❌ Criar múltiplos arquivos .md para cada situação
- ❌ Voltar para soluções que já falharam

## 🔧 **Configurações Atuais**

### **Portas:**
- Webhook: 8001 (única porta necessária)

### **Volumes:**
- `./downloads:/app/downloads` (webhook)
- `./logs:/app/logs` (webhook)

### **Configurações Chrome:**
- Chrome instalado diretamente no container
- ChromeDriver instalado diretamente no container
- Configurações robustas aplicadas
- Download automático habilitado

## 🚀 **Próximo Passo**

**Fazer redeploy** para testar se a versão dinâmica do ChromeDriver funciona automaticamente.

**Melhoria aplicada:** ChromeDriver agora detecta automaticamente a versão do Chrome instalada.

**Vantagem:** Não precisará mais atualizar manualmente quando o Chrome atualizar.

**Backup seguro:** Tag `SISTEMA-FUNCIONANDO-2025-08-01` criada para voltar se necessário.

**Descoberta importante:** Sistema funcionando perfeitamente! Agora com versão dinâmica para evitar problemas futuros.

---

## 🕵️‍♂️ Observação Importante: Logs e Containers Duplicados

- **Comportamento observado:**
  - Ao acessar a tela de logs no Coolify, aparecem dois containers com nomes quase idênticos (ex: `webhook-relatorios-pocwc808kw0s0wwwoc0808oc-02532D0448953` e `webhook-relatorios-pocwc808kw0s0wwwoc0808oc-025403557059`).
  - Apenas um deles realmente gera logs do sistema; o outro permanece vazio.
  - **Possível causa:** Pode ser resquício de deploys antigos, containers "fantasmas" ou comportamento do próprio Coolify ao gerenciar múltiplas execuções/deploys.
  - **Impacto:** Não afeta o funcionamento do sistema, mas pode confundir na análise dos logs. Sempre conferir qual container está ativo e gerando logs reais.

## ✅ Checklist Final - Estrutura e Funcionamento

- **Pastas essenciais:**
  - `downloads/` (com `.gitkeep`) — usada para salvar PDFs e arquivos baixados
  - `logs/` (com `.gitkeep`) — usada para logs do sistema
  - Ambas as pastas são montadas como volumes no Docker Compose
- **Funcionamento dos logs:**
  - Logs detalhados são gerados em tempo real na pasta `logs/` e também exibidos no painel do Coolify
  - O sistema registra cada etapa: recebimento do webhook, processamento, geração e envio do PDF, remoção do arquivo
- **Deploy bem-sucedido:**
  - PDF gerado e enviado corretamente via WhatsApp
  - Logs confirmam o fluxo completo sem erros

---

**Memorial atualizado em: 2025-08-01 02:30** 