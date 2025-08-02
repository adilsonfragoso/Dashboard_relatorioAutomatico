# 🔧 Configuração do Arquivo .env

## 📋 **Variáveis Necessárias**

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do Banco de Dados MySQL
DB_HOST=pma.linksystems.com.br
DB_USER=adseg
DB_PASSWORD=Define@4536#8521
DB_NAME=litoral
DB_CHARSET=utf8mb4

# Configurações de Login do Painel
LOGIN_URL=https://painel.litoraldasorte.com
LOGIN_EMAIL=seu_email_aqui
LOGIN_PASSWORD=sua_senha_aqui
```

## ⚠️ **Importante:**

1. **Substitua** `seu_email_aqui` pelo email real de login
2. **Substitua** `sua_senha_aqui` pela senha real de login
3. **Não commite** o arquivo `.env` no Git (já está no .gitignore)

## 🧪 **Para Teste:**

Se você não tiver as credenciais reais, pode usar credenciais de teste temporárias para verificar se o sistema funciona.

---

**Última atualização:** 2025-08-01 23:38 