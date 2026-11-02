## Why

Ao planejar a construção de um móvel, saber apenas a lista de peças não é suficiente para comprar o material: é indispensável saber quantas chapas inteiras (geralmente 2750 x 1830 mm no padrão brasileiro) serão consumidas e como dispor as peças minimizando sobras. Esta mudança implementa o algoritmo de plano de corte 2D (guillotine/shelf bin-packing) no servidor MCP e orienta a skill a gerar o cálculo de aproveitamento de chapa.

## What Changes

- Implementação do módulo `cutlist_optimizer.py` no servidor MCP, contendo algoritmo 2D para encaixe de peças em chapas retangulares.
- Suporte a espessura da lâmina de serra (*kerf*, padrão 4mm), margem de refile de chapa (padrão 10mm) e opção de rotação de peças (respeito a sentido de veio para MDF madeirado).
- Exposição da ferramenta `calculate_cutting_plan` no servidor MCP.
- Atualização da Skill de Marcenaria para calcular o plano de corte e apresentar métricas de aproveitamento (% de uso da chapa) e sobras utilizáveis.

## Capabilities

### New Capabilities
<!-- Nenhuma capacidade totalmente nova; estendendo as duas existentes -->

### Modified Capabilities
- `mcp-server-leomadeiras`: Adiciona a ferramenta `calculate_cutting_plan` para cálculo determinístico de corte 2D de chapas.
- `marcenaria-assistant-skill`: Adiciona a regra de estimativa de aproveitamento de chapas a partir da lista de corte (BOM).

## Impact

- Novos módulos em `mcp-server/src/cutlist_optimizer.py`.
- Nova ferramenta registrada em `mcp-server/src/server.py`.
- Atualização da skill em `skill/` e `.agent/skills/marcenaria-assistant/`.
- Sem quebra de compatibilidade com as ferramentas existentes.
