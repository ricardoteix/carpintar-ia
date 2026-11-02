## Why

O visualizador 3D apresentou duas limitações críticas:
1. O modelo 3D da Cadeira Krat possui peças flutuantes (ripas do encosto e assento sem apoio estrutural) e peças colidindo no mesmo plano X (pernas e braços).
2. O visualizador estava restrito a 3 presets estáticos com carregamento manual de arquivo, enquanto o usuário precisa que qualquer móvel planejado durante a conversa no chat seja visualizado automaticamente no navegador.

## What Changes

- Correção estrutural da Cadeira Krat em `viewer/app.js` e `mcp-server/src/project_3d.py`, incluindo:
  - Compensação de planos para evitar sobreposição (face externa dos braços e travessas com montantes verticais).
  - Adição dos suportes inclinados do assento e dos montantes estruturais do encosto (fim das peças flutuantes).
- Implementação de sincronização automática entre o chat e o visualizador através de `viewer/current_project.js`.
- Criação de geradores 3D universais em `mcp-server/src/project_3d.py` (estantes, mesas/bancadas, armários com gavetas/portas, nichos e caixarias).
- Adição da ferramenta MCP `preview_furniture_3d` que gera o modelo 3D do móvel discutido e atualiza a cena ativa do visualizador.
- Atualização do visualizador `viewer/index.html` e `viewer/app.js` para priorizar e recarregar automaticamente o projeto atual do chat com indicador visual ("🌟 Projeto do Chat").

## Capabilities

### New Capabilities
<!-- Nenhuma nova capacidade raiz criada -->

### Modified Capabilities
- `visualizador-3d-app`: Suporta carregamento em tempo real do projeto ativo do chat via script local (`current_project.js`), recarregamento dinâmico sem CORS e modelo corrigido da Cadeira Krat.
- `mcp-server-leomadeiras`: Expõe a ferramenta `preview_furniture_3d` que constrói a cena 3D completa de qualquer tipo de móvel e salva diretamente como projeto ativo no visualizador.
- `marcenaria-assistant-skill`: Instrui o agente a gerar a visualização 3D automaticamente para qualquer projeto proposto na conversa.

## Impact

- `viewer/current_project.js` gerado dinamicamente para permitir abertura direta no navegador via `file://`.
- Atualização em `viewer/app.js`, `viewer/index.html`, `mcp-server/src/project_3d.py` e `mcp-server/src/server.py`.
- Nenhuma dependência externa adicional.
