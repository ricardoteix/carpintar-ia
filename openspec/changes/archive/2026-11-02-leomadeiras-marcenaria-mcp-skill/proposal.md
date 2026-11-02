## Why

Projetar e construir móveis ou projetos de marcenaria exige decompor uma ideia em peças individuais (BOM), deduzir insumos "invisíveis" de montagem (parafusos, fitas de borda, cola, suportes) e encontrar materiais reais com preços e dimensões disponíveis no mercado. Esta mudança introduz uma solução em duas camadas (um MCP Server em Python e uma Skill de Marcenaria) que conecta o raciocínio prático de carpintaria aos dados de catálogo e produtos da Leo Madeiras.

## What Changes

- Criação de um servidor MCP local em Python (`mcp-server/`) utilizando FastMCP e httpx para consultar os endpoints de busca e sugestões de `leomadeiras.com.br`, além de auxiliar na recomendação de ferragens/kits de montagem.
- Criação de uma Skill de Marcenaria (`skill/`) contendo diretrizes, fórmulas de folga/desconto para MDF/compensado, regras para estimativa de insumos e orçamentação automatizada.
- Definição da estrutura inicial de documentação de apoio e referências técnicas (tabelas de ferragens e espessuras).

## Capabilities

### New Capabilities
- `mcp-server-leomadeiras`: Servidor local compatível com o protocolo MCP que expõe ferramentas para pesquisar produtos, obter sugestões e recomendar kits de ferragens utilizando a API pública da Leo Madeiras.
- `marcenaria-assistant-skill`: Skill especializada que guia o agente na decomposição de projetos de marcenaria em peças de corte e kit de insumos de montagem, acionando o MCP para orçar itens.

### Modified Capabilities
<!-- Nenhuma capacidade existente modificada -->

## Impact

- Novos diretórios no repositório: `mcp-server/` e `skill/`.
- Dependências Python: `mcp` (FastMCP), `httpx`, `pydantic`.
- Nenhuma alteração disruptiva em código pré-existente (projeto novo).
