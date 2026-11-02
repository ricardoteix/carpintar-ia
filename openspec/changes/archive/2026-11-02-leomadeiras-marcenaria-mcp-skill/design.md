## Context

O usuário deseja projetar móveis e estruturas de marcenaria de forma assistida. Atualmente, a consulta de materiais, espessuras e preços da Leo Madeiras é feita manualmente através da interface web. A solução consiste em desacoplar a lógica de consulta técnica (através de um MCP Server local em Python) da lógica de marcenaria e engenharia de produto (através de uma Skill com conhecimento especializado de carpintaria).

## Goals / Non-Goals

**Goals:**
- Implementar um servidor local MCP em Python (`mcp-server/`) utilizando `FastMCP` e `httpx` assíncrono.
- Integrar com os endpoints públicos da Leo Madeiras:
  - `https://www.leomadeiras.com.br/api/suggestions?q={query}`
  - `https://www.leomadeiras.com.br/api/search?q={query}&sort=relevance&from={from}&to={to}`
- Fornecer ferramenta de auxílio na montagem de kit de insumos/ferragens (parafusos 3.5x16, 4.0x40, dobradiças 35mm, fita de borda, cola, tapa-furos).
- Desenvolver a Skill (`skill/`) com diretrizes para cálculo de decomposição de peças (BOM), dedução de folgas, fitas de borda e orçamentação através das tools do MCP.
- Documentar tabelas de referência de marcenaria em `skill/references/`.

**Non-Goals:**
- Algoritmo complexo de corte 2D (nesting) nesta fase (planejado para a Fase 2).
- Visualizador 3D com Three.js/WebGL nesta fase (planejado para a Fase 3).
- Realização de checkout ou autenticação com dados sensíveis do cliente na Leo Madeiras.

## Decisions

1. **Linguagem do MCP: Python com FastMCP**
   - *Decisão*: Utilizar `mcp.server.fastmcp.FastMCP` com cliente assíncrono `httpx`.
   - *Justificativa*: Simplicidade de código, facilidade de manutenção pelo usuário, suporte nativo a tipagem Pydantic e execução direta via `uv` ou `python -m`.
   - *Alternativas*: Node.js/TypeScript (descartado por preferência expressa do usuário por Python).

2. **Separação de Camadas (MCP Server vs Skill)**
   - *Decisão*: Manter o MCP Server estritamente focado em dados/APIs e utilitários auxiliares determinísticos; deixar a interação conversacional e a engenharia de montagem para a Skill.
   - *Justificativa*: Permite reaproveitar o MCP Server em qualquer outro cliente MCP sem amarrar regras rígidas de prompt no código Python.

3. **Resiliência a Falhas de Rede e Formatação da Leo Madeiras**
   - *Decisão*: Sanitizar o payload retornado da API da Leo Madeiras extraindo apenas os campos essenciais (`id`, `name`, `slug`, `price`, `listPrice`, `brand`, `category`, `stock`, `facets`) para não sobrecarregar o contexto do LLM.
   - *Justificativa*: A API da Leo Madeiras devolve URLs de imagens pesadas e estruturas aninhadas que gastam tokens desnecessariamente.

## Risks / Trade-offs

- **[Risco] Mudança não anunciada nos endpoints da Leo Madeiras** → *Mitigação*: Encapsular todas as chamadas no módulo `leo_client.py` com tratamento de erro e fallbacks claros quando a API retornar status diferente de 200.
- **[Risco] Variação regional de preços/estoque** → *Mitigação*: A API pública retorna preços base gerais do catálogo nacional; explicitar ao usuário que preços e estoque podem variar conforme a filial de retirada ou CEP selecionado.
