# Dashboard de Gerenciamento de Rifas

Esta é uma versão isolada da dashboard do sistema de gerenciamento de rifas, projetada para rodar independentemente no Coolify ou qualquer outro ambiente Docker.

## 📋 Estrutura do Projeto

```
dashboard/
├── main.py                 # Aplicação FastAPI principal
├── requirements.txt        # Dependências Python
├── Dockerfile             # Configuração Docker
├── docker-compose.yml     # Orquestração Docker
├── env.example           # Exemplo de variáveis de ambiente
├── README.md             # Esta documentação
├── static/               # Arquivos estáticos
│   ├── dashboard.html    # Página principal
│   ├── css/
│   │   ├── common.css    # Estilos comuns
│   │   └── dashboard.css # Estilos específicos da dashboard
│   ├── js/
│   │   └── dashboard.js  # JavaScript da dashboard
│   └── img/              # Imagens (criar conforme necessário)
└── scripts/              # Scripts externos (opcional)
```

## 🚀 Funcionalidades

### Endpoints da API

1. **GET /** - Página principal da dashboard
2. **GET /api/dashboard/extracoes-recentes** - Lista extrações ativas
3. **POST /api/dashboard/enviar-link-edicao/{edicao}** - Envia link via WhatsApp
4. **POST /api/dashboard/gerar-relatorio/{edicao}** - Gera relatório PDF
5. **GET /api/dashboard/verificar-pdf/{edicao}** - Verifica se PDF existe
6. **GET /api/dashboard/download-pdf/{edicao}** - Download do PDF
7. **GET /api/dashboard/status-heroku** - Status do servidor Heroku

### Características da Dashboard

- ✅ **Sincronização em tempo real** - Atualizações automáticas a cada 15s
- ✅ **Monitoramento de status** - Verifica status do servidor Heroku
- ✅ **Geração automática de relatórios** - PDFs gerados automaticamente para rifas 100%
- ✅ **Interface responsiva** - Funciona em desktop e mobile
- ✅ **Estados visuais** - Indicadores de processamento e status
- ✅ **Modal de ações** - Envio de WhatsApp e links diretos

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Docker e Docker Compose
- MySQL/MariaDB com as tabelas necessárias
- Acesso ao banco de dados

### 1. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e configure suas variáveis:

```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
DB_HOST=seu_host_mysql
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=seu_banco
DB_CHARSET=utf8mb4
```

### 2. Executar com Docker Compose

```bash
# Construir e iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### 3. Executar Localmente (Desenvolvimento)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python main.py
```

A aplicação estará disponível em: `http://localhost:8001`

## 📊 Banco de Dados

### Tabelas Necessárias

A dashboard depende das seguintes tabelas no MySQL:

1. **extracoes_cadastro** - Dados das extrações
2. **premiacoes** - Informações das premiações
3. **logs_andamento** - Logs do servidor Heroku

### Estrutura Mínima

```sql
-- Tabela extracoes_cadastro
CREATE TABLE extracoes_cadastro (
    id INT PRIMARY KEY AUTO_INCREMENT,
    edicao INT,
    sigla_oficial VARCHAR(50),
    extracao VARCHAR(50),
    link TEXT,
    status_cadastro VARCHAR(20),
    status_link VARCHAR(20),
    error_msg TEXT,
    andamento VARCHAR(10),
    status_rifa VARCHAR(20),
    data_sorteio DATE
);

-- Tabela premiacoes
CREATE TABLE premiacoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sigla VARCHAR(50),
    horario VARCHAR(20),
    imagem_path VARCHAR(255)
);

-- Tabela logs_andamento
CREATE TABLE logs_andamento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data_hora DATETIME,
    log_status VARCHAR(20)
);
```

## 🔧 Configuração no Coolify

### 1. Criar Aplicação

1. Acesse o Coolify
2. Clique em "New Application"
3. Selecione "Docker Compose"
4. Conecte seu repositório

### 2. Configurar Variáveis de Ambiente

No Coolify, adicione as seguintes variáveis de ambiente:

- `DB_HOST` - Host do MySQL
- `DB_USER` - Usuário do MySQL
- `DB_PASSWORD` - Senha do MySQL
- `DB_NAME` - Nome do banco
- `DB_CHARSET` - Charset (opcional, padrão: utf8mb4)

### 3. Configurar Volumes (Opcional)

Se precisar acessar scripts externos ou downloads:

- `./scripts:/app/scripts` - Para scripts externos
- `./downloads:/app/downloads` - Para arquivos PDF

### 4. Deploy

1. Configure a porta 8001
2. Clique em "Deploy"
3. Acesse a aplicação via URL fornecida

## 📁 Arquivos Importantes

### main.py
- Aplicação FastAPI principal
- Todos os endpoints da API
- Configuração do banco de dados
- Servir arquivos estáticos

### static/dashboard.html
- Interface principal da dashboard
- Estrutura HTML responsiva
- Integração com CSS e JavaScript

### static/css/dashboard.css
- Estilos específicos da dashboard
- Animações e estados visuais
- Design responsivo

### static/js/dashboard.js
- Lógica JavaScript completa
- Sincronização em tempo real
- Monitoramento de status
- Geração automática de relatórios

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco**
   - Verifique as variáveis de ambiente
   - Confirme se o banco está acessível

2. **Scripts não encontrados**
   - Verifique se a pasta `scripts/` existe
   - Configure volumes no Docker se necessário

3. **PDFs não gerados**
   - Verifique permissões de escrita
   - Confirme se os scripts estão funcionando

4. **Dashboard não atualiza**
   - Verifique logs da aplicação
   - Confirme se a tabela `logs_andamento` existe

### Logs

```bash
# Ver logs do container
docker-compose logs dashboard

# Ver logs em tempo real
docker-compose logs -f dashboard
```

## 🔄 Atualizações

Para atualizar a aplicação:

```bash
# Parar aplicação
docker-compose down

# Reconstruir imagem
docker-compose build --no-cache

# Iniciar novamente
docker-compose up -d
```

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique os logs da aplicação
2. Confirme configuração do banco de dados
3. Teste conectividade com MySQL
4. Verifique variáveis de ambiente

## 🎯 Próximos Passos

- [ ] Adicionar autenticação
- [ ] Implementar cache Redis
- [ ] Adicionar métricas e monitoramento
- [ ] Implementar backup automático
- [ ] Adicionar testes automatizados

---

**Versão**: 1.0.0  
**Última atualização**: Dezembro 2024  
**Compatibilidade**: Python 3.11+, MySQL 5.7+ 