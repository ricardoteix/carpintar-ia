## 1. Algoritmo de Otimização de Corte 2D

- [x] 1.1 Implementar `mcp-server/src/cutlist_optimizer.py` com classes e funções de Guilhotina 2D (corte reto, kerf e refile)
- [x] 1.2 Implementar suporte a restrição de sentido de veio (`can_rotate`) e métricas de aproveitamento de área

## 2. Ferramenta MCP e Testes

- [x] 2.1 Registrar a ferramenta `calculate_cutting_plan` em `mcp-server/src/server.py`
- [x] 2.2 Criar teste automatizado em `mcp-server/tests/test_cutting_plan.py` validando encaixe de peças e cálculo de sobras

## 3. Atualização da Skill e Validação

- [x] 3.1 Atualizar `skill/SKILL.md` e `.agent/skills/marcenaria-assistant/SKILL.md` incluindo o plano de corte no fluxo do assistente
- [x] 3.2 Atualizar documentação `mcp-server/README.md` com a nova ferramenta
- [x] 3.3 Validar simulação completa com a Cadeira Krat e Armário
