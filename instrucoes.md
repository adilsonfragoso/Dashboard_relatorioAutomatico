# 📋 Instruções de Trabalho - Projeto RelatorioWhats

## 🎯 **Diretrizes Gerais**

use sempre python 3.12.4
prepare sempre o ambiente virtual para cada novo projeto.
Durante produção ou quando preparar para vps, se tiver algum arquivo .md expondo senhas e dados confidenciais, coloque no .gitignore


### **📝 Gestão de Documentação**
- ✅ **Evitar reescrita desnecessária** - Não reescrever arquivos `.md` inteiros para pequenas atualizações
- ✅ **Usar memorial centralizado** - Criar e manter apenas um memorial de alterações


### **🔍 Memorial de Alterações**
- ✅ **Criar memorial único** - Para trabalhar e avaliar alterações
- ✅ **Registrar tentativas** - Cada tentativa deve ser registrada com:
  - O que foi feito
  - Erro que ocorreu
  - Data/hora da tentativa
- ✅ **Evitar loops** - Evite repetir soluções que já falharam, a não ser que ache importante devido a outras alterações.
- ✅ **Histórico completo** - Manter histórico, não substituir informações

## 🚀 **Estratégias de Resolução**

### **📚 Projetos de Referência**
- ✅ **Valorizar projetos funcionais** - Quando informar projeto que funciona em Docker/Coolify
- ✅ **Estudar modelo** - Entender como funciona e usar como referência


### **🧪 Arquivos de Teste**
- ✅ **Adicionar ao .gitignore** - Arquivos de teste que não serão usados no Coolify
- ✅ **Reutilizar testes** - Verificar se já existe arquivo similar antes de criar novo

## ⚠️ **Restrições Importantes**

### **🔒 Automação Original**
- ❌ **NUNCA alterar** a automação em si dos scripts `.py`
- ❌ **NUNCA modificar** clicks nas páginas dentro das automações e maneiras como elas funcionam.
- ✅ **Manter lógica** original testada e funcionando

### **📁 Gestão de Arquivos**
- ❌ **Evitar criação excessiva** de arquivos `.md`
- ✅ **Manter projeto limpo** e organizado

## 📊 **Exemplos de Problemas Evitados**

### **🔌 Conflitos de Porta**
- **Problema:** Erro de porta sendo usada
- **Solução:** Registrar no memorial para evitar repetição
- **Resultado:** Evita trabalho desnecessário

### **🔄 Loops de Alterações**
- **Problema:** Voltar a fazer coisas que já falharam mesmo sem ter mudado outros parametros
- **Solução:** Memorial com histórico completo
- **Resultado:** Não sair do problema


### **Preparação para VSP**
- **Inicialemnte:** Todo projeto deve ser preparado para rodar localmente no pc windows com ambientes adequados e mantendo os projeto mais parecido possível com o necessario para docker no coolify.
- **Credencias:** nunca insira dados login e senha diretamente nos arquivos, prepare o .env para isso
- **Após testes:** Depois de tudo testado, rodando certinho em local, quando solicitado deverá preparar tudo para rodar no docker
 para coolify. dados de acesso, senha e login serão configurados na seção "Production Enviroment Variables' do coolify. Verifique requirements se está atualizado de acordo com o projeto.


---

**📋 Estas instruções garantem eficiência e organização no desenvolvimento!**
