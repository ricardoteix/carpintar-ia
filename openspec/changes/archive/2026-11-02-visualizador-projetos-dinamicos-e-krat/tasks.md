## 1. Correção Estrutural da Cadeira Krat

- [x] 1.1 Corrigir sobreposições nos planos X das laterais em `viewer/app.js` e em `mcp-server/src/project_3d.py`
- [x] 1.2 Adicionar suportes inclinados do assento e montantes de encosto (eliminando ripas flutuantes)
- [x] 1.3 Validar geometria com teste e renderização

## 2. Sincronização Dinâmica no Frontend

- [x] 2.1 Adicionar inclusão de `current_project.js` em `viewer/index.html` via tag script
- [x] 2.2 Atualizar `viewer/app.js` para detectar `window.CURRENT_PROJECT`, adicioná-lo ao menu e selecioná-lo automaticamente
- [x] 2.3 Adicionar botão "🔄 Recarregar Projeto do Chat" no visualizador com timestamp para recarga dinâmica

## 3. Gerador Universal de Móveis 3D e Ferramenta MCP

- [x] 3.1 Expandir `mcp-server/src/project_3d.py` com geradores para Cadeira Krat, Estantes, Mesas, Balcões e Armários com gavetas
- [x] 3.2 Implementar função `save_current_project` que gera `viewer/current_project.js` e `viewer/current_project.json`
- [x] 3.3 Registrar ferramenta `preview_furniture_3d` em `mcp-server/src/server.py`

## 4. Atualização da Skill e Testes

- [x] 4.1 Atualizar `skill/SKILL.md` e `.agent/skills/marcenaria-assistant/SKILL.md` para acionar `preview_furniture_3d` automaticamente
- [x] 4.2 Criar teste automatizado em `mcp-server/tests/test_dynamic_project.py`
- [x] 4.3 Gerar a Cadeira Krat corrigida diretamente em `viewer/current_project.js` para teste imediato do usuário
