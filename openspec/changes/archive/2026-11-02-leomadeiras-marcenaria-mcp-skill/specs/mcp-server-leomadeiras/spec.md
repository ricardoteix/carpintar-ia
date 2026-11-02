## ADDED Requirements

### Requirement: Busca de Produtos na Leo Madeiras
O servidor MCP SHALL expor uma ferramenta `search_materials` que consulta a API de busca da Leo Madeiras e retorna uma lista simplificada de produtos com nome, preço, dimensões, estoque e link.

#### Scenario: Consulta com termo válido
- **WHEN** o cliente MCP invoca `search_materials` com `query="Pinus"` e `limit=10`
- **THEN** o servidor retorna produtos filtrados contendo `id`, `name`, `price`, `slug` e facetas relevantes

#### Scenario: Nenhum produto encontrado
- **WHEN** o cliente MCP invoca `search_materials` com um termo inexistente
- **THEN** o servidor retorna uma lista vazia sem lançar exceção não tratada

### Requirement: Sugestões de Termos da Leo Madeiras
O servidor MCP SHALL expor uma ferramenta `suggest_terms` que consulta o endpoint de sugestões rápidas da Leo Madeiras.

#### Scenario: Obtenção de sugestões automáticas
- **WHEN** o cliente MCP invoca `suggest_terms` com `query="MDF"`
- **THEN** o servidor retorna a lista de termos e categorias sugeridas pela API

### Requirement: Recomendação de Kit de Ferragens
O servidor MCP SHALL expor uma ferramenta `recommend_hardware_kit` que calcula a lista de ferragens e insumos básicos recomendados com base no tipo de móvel e número de componentes.

#### Scenario: Cálculo de kit para móvel com portas e gavetas
- **WHEN** o cliente MCP invoca `recommend_hardware_kit` com número de portas e gavetas especificadas
- **THEN** o servidor retorna o quantitativo sugerido de dobradiças 35mm, corrediças telescópicas, parafusos (3.5x16 e 4.0x40), fita de borda e tapa-furos
