# Pasta de Scripts

Esta pasta é opcional e deve conter scripts externos que a dashboard pode executar.

## Scripts Necessários (se usados)

1. **novo_chamadas_group_latest.py** - Script para envio de WhatsApp
2. **relatorio_v1.py** - Script para geração de relatórios PDF

## Como Adicionar Scripts

1. Copie os scripts do projeto principal para esta pasta
2. Certifique-se de que os scripts têm permissões de execução
3. Os scripts devem ser compatíveis com Python 3.11+

## Estrutura Recomendada

```
scripts/
├── novo_chamadas_group_latest.py
├── relatorio_v1.py
└── README.md
```

## Configuração Docker

Se usar scripts externos, configure o volume no docker-compose.yml:

```yaml
volumes:
  - ./scripts:/app/scripts
```

## Notas

- Os scripts são executados via subprocess
- Certifique-se de que todas as dependências dos scripts estão instaladas
- Os scripts devem retornar códigos de saída apropriados (0 para sucesso)
- Timeouts são configurados para evitar travamentos 