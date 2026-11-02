## 1. Setup do Projeto MCP Python

- [x] 1.1 Criar diretório `mcp-server/` e definir `requirements.txt` / `pyproject.toml` com `mcp>=1.0.0`, `httpx`, `pydantic`
- [x] 1.2 Configurar estrutura de pastas `mcp-server/src/` com ponto de entrada e módulos

## 2. Cliente HTTP Leo Madeiras & Regras

- [x] 2.1 Implementar `leo_client.py` com métodos assíncronos para busca (`/api/search`) e sugestões (`/api/suggestions`)
- [x] 2.2 Implementar `rules.py` com funções para cálculo de kits de ferragens básicas (dobradiças, corrediças, parafusos, fita)

## 3. Servidor MCP e Ferramentas

- [x] 3.1 Implementar `server.py` inicializando FastMCP e registrando `search_materials`, `suggest_terms` e `recommend_hardware_kit`
- [x] 3.2 Implementar script de teste ou execução direta para validar comunicação com a API da Leo Madeiras

## 4. Skill de Marcenaria

- [x] 4.1 Criar diretório `skill/` com `SKILL.md` detalhando as instruções de raciocínio de marcenaria e integração com o MCP
- [x] 4.2 Criar arquivos de referência técnica em `skill/references/` (medidas padrão, tipos de chapas e tabela de ferragens)
- [x] 4.3 Disponibilizar a skill também no formato padrão de skills do agente em `.agent/skills/marcenaria-assistant/`

## 5. Documentação e Validação Final

- [x] 5.1 Criar `mcp-server/README.md` com instruções de como rodar e registrar o MCP no Antigravity/Claude
- [x] 5.2 Testar uma consulta completa de projeto (nicho/armário) validando o fluxo de ponta a ponta
