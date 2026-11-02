# Tarefas de Implementação: Manual de Montagem e Guia de Ferramentas

## 1. Servidor MCP e Lógica de Negócio
- [x] 1.1 Criar função de dedução de ferramentas necessárias em `rules.py` (essenciais, opcionais e EPIs).
- [x] 1.2 Implementar geradores de manual de montagem passo a passo em `project_3d.py` para todos os móveis (`krat`, `armario`, `nicho`, `estante`).
- [x] 1.3 Adicionar a tool `generate_assembly_manual` no FastMCP em `server.py`.
- [x] 1.4 Criar testes automatizados para a geração de manual e ferramentas em `mcp-server/tests/`.

## 2. Visualizador 3D e Interface
- [x] 2.1 Adicionar botão `📖 Manual de Montagem` na barra de ferramentas em `viewer/index.html`.
- [x] 2.2 Criar modal/painel lateral do manual com visualização de ferramentas, checklist de passos e fases em `viewer/style.css` e `viewer/app.js`.
- [x] 2.3 Implementar botão de download do manual em formato Markdown (`.md`).
- [x] 2.4 Implementar regras `@media print` para exportação limpa em PDF via impressão do navegador.

## 3. Skill e Documentação
- [x] 3.1 Atualizar `skill/SKILL.md` para incluir a etapa de ferramentas e oferta de manual de montagem.
- [x] 3.2 Atualizar especificações OpenSpec e validar a solução.
