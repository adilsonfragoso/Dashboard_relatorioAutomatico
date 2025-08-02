# 📋 Instruções sobre este projeto

"Vamos preparar tudo para rodar em docker coolify

### **outras informações**
 - lembre se , o webhook server deverá rodar na porrta 8010 pois lá temos outro servidor em outro docker que roda na porta 8001
 - lembre se de preparar para que os arquivos não exibam dados de login e acesso, os mesmos deverá estar no enviroment do docker coolify, só me informe quais dados devo adiconar lá. 
 - prepare os arquivos com logs para que durante a implantação possamos identificar erros.
- mantenha atualizado o arquivo @dados_webhook.md inclusive com o link webhook a ser usado. Um detalhe importante sobre esse link webhook é que não sei se vai ser localhost:8010, pois a aplicação que irá chamar esse webhook está em outro docker, porém no mesmo servidor coolify
- lembre se que relatorio_V2_vps foi readaptado para rodar localmente no windows e precisa estar preparado para rodar no docker.
- não esqueça qeu o main esta hardcoded , as senhas devem estar no enviroment do docker
- antes de continuar, na dashboard resolve uma coisa: 
             retire o menu ali de cima. Editar, Edições e Premiações já que será uma pagina solo frontend

