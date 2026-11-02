## Why

Para quem constrói móveis (tanto iniciantes quanto marceneiros experientes), interpretar apenas uma tabela de medidas e cortes pode ser abstrato e propenso a erros de montagem. Uma visualização 3D interativa com efeito de "visão explodida" permite inspecionar cada peça no espaço tridimensional, entender a ordem de montagem e validar as folgas e junções antes de cortar a primeira chapa de madeira.

## What Changes

- Criação de uma aplicação web standalone leve em `viewer/` utilizando Three.js e OrbitControls, com renderização de materiais de madeira/MDF, iluminação de estúdio e controle deslizante de visão explodida (0 a 100%).
- Suporte a presets embutidos (Armário Aéreo de 2 Portas, Nicho de Parede e a clássica Cadeira Krat de Gerrit Rietveld).
- Implementação da ferramenta `export_3d_project` no MCP Server para exportar os modelos 3D dos móveis diretamente para o visualizador.
- Atualização da Skill de Marcenaria para disponibilizar o link/arquivo do modelo 3D ao concluir o projeto.

## Capabilities

### New Capabilities
- `visualizador-3d-app`: Aplicação web interativa 3D com OrbitControls, slider de visão explodida, inspeção de dimensões das peças e alternância de materiais (MDF Branco / Pinus).

### Modified Capabilities
- `mcp-server-leomadeiras`: Adiciona ferramenta para exportar a cena 3D do projeto em formato JSON / HTML navegável.
- `marcenaria-assistant-skill`: Guia o agente a fornecer o arquivo ou link do projeto 3D ao usuário após detalhar o plano de montagem.

## Impact

- Novo diretório `viewer/` contendo a aplicação frontend HTML/CSS/JS (Three.js sem necessidade de build complexo, rodando diretamente no navegador).
- Nova ferramenta registrada em `mcp-server/src/server.py`.
