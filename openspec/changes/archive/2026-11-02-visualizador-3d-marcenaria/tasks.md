## 1. Estrutura da Aplicação Web 3D

- [x] 1.1 Criar diretório `viewer/` com `index.html`, `style.css` e `app.js` configurando Three.js e OrbitControls
- [x] 1.2 Criar layout de interface com painel superior (seletor de projetos, slider de explosão, botão de reset e alternância de material)

## 2. Modelagem 3D, Interatividade e Presets

- [x] 2.1 Implementar sistema de peças 3D com texturas procedurais/materiais para Pinus Natural e MDF Branco Texturizado
- [x] 2.2 Implementar interpolação suave de visão explodida controlada pelo slider (0% a 100%)
- [x] 2.3 Criar presets interativos: Cadeira Krat de Gerrit Rietveld, Armário Aéreo de 2 Portas e Nicho de Parede
- [x] 2.4 Implementar raycasting com mouse para destacar e exibir detalhes da peça selecionada no painel lateral

## 3. Integração no MCP Server e Skill

- [x] 3.1 Implementar gerador de modelos de projeto 3D em `mcp-server/src/project_3d.py`
- [x] 3.2 Adicionar ferramenta `export_3d_project` em `mcp-server/src/server.py`
- [x] 3.3 Atualizar a skill de marcenaria em `skill/SKILL.md` e `.agent/` com instruções de visualização 3D

## 4. Validação e Documentação

- [x] 4.1 Criar teste em `mcp-server/tests/test_3d_export.py` validando geração de coordenadas e arquivos 3D
- [x] 4.2 Atualizar `mcp-server/README.md` e `viewer/README.md` com instruções de uso no navegador
