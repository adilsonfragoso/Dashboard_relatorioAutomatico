# 📋 Instruções sobre este projeto

" ATENÇÃO:  Este é um informativo que não pode ser modificado. Qualquer anotação ou alteração, siga @instrucoes.md

## 🎯 **Diretrizes Gerais**


### **📝 Scripts**
- ✅ **relatorio_v2_vps.py** - Cópia identica de uma que está rodando perfeitamente em outro docker coolify
- ✅ **dashboard.html** - Ainda não está rodando em docker, roda em ambiente local pc, mas, agora será preparada para rodar em docker coolify.
- ✅ **webhook_server** - Cópia identica de uma que está rodando perfeitamente em outro docker coolify juntamente com relatorio_v2_vps.py citado acima.


### **Objetivo desse projeto**
- ✅ **dashboard** - Mostra em tempo real o andamento das rifas, lê dados do banco de dados para exibir informações de rifas ativa e seu andamento em %
sobre pdf nesse script, ler anotações "nota 1" em anexo ao final
- ✅ **relatorio_v2_vps.py** - Será acionado através do webhook_server.py, será necessário ter uma pasta para amarzenar o relatorio gerado. ler "nota 2" em anexo ao final desse .md, no outro projeto o objetivo era gerar o pdf e devolver ao usuario que solicitava pelo whatsapp.
- ✅ **webhook_server.py** - Esse script foi preparado para receber uma mensagem do whatsapp, neste caso agora, para esse projeto, retire as informações de api do evolution. não será mais dessa forma. Ele será um webhook que receberá dados através de outra aplicação, continuará ouvindo, mas, não irá esperar de um celular. Ele agirá da mesma forma em relação a chamar o relatorio_v2_vps com a edição a ser processada, mas, o pdf gerado não será retornado ao solicitante, será amarzenado localmente nesse projeto. Não precisará consultar informações no banco de dados como atualmente antes de seguir para chamar relatorio_v2_vps
❌ **leitura de informações prévias no banco de dados sobre a edição solicitada** isso não será mais necessário.
❌ **API evolution whatsapp** não será mais necessário, irá receber solicitação de outra aplicação.

  Se possível, veja que criei um .env que deverá ser adicionado ao .gitignore se ainda não foi. Eu gostaria de preparar cada aplicação que requer dados login e senha, de forma que busque em .env para teste local e ao mesmo tempo esteja preparado para buscar esses dados no enviroment embutido no coolify



### **outras informações**
 para webhook_server não use a porta 8001, use a porta 8010


## **anotações**

### **nota 1**
-inicialmente de dashboard.html precisamos tirar a maneira como carrega o pdf, como gera o pdf ou qualquer outra coisa em relação ao pdf. só deixe a coluna onde deverá ser exibido o arquivo, iremos tratar disso posteriormente.

### **nota 2**
-verifique o script relatorio_v2_vps.py, entendo que ele esteja deletando o arquivo pdf gerado. Nesse script, esse pdf gerado não irá retornar para whatsapp solicitado, será gravado numa pasta dentro deste docker que deverá ser criada ou conforme regras da aplicação.

