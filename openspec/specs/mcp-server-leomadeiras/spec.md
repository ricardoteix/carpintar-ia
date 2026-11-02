# mcp-server-leomadeiras Specification

## Purpose
TBD - created by archiving change leomadeiras-marcenaria-mcp-skill. Update Purpose after archive.
## Requirements
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

### Requirement: Otimização de Plano de Corte 2D
O servidor MCP SHALL expor uma ferramenta `calculate_cutting_plan` que recebe uma lista de peças com dimensões e quantidades e calcula a quantidade mínima de chapas necessárias, considerando folga de serra (*kerf*) e margem de refile.

#### Scenario: Cálculo de corte com chapa padrão de MDF
- **WHEN** o cliente invoca `calculate_cutting_plan` com peças de um móvel e dimensões de chapa (2750 x 1830 mm)
- **THEN** o servidor retorna o total de chapas necessárias, percentual de aproveitamento e disposição das peças por chapa

#### Scenario: Respeito à orientação de veio
- **WHEN** uma peça possui o parâmetro `can_rotate=False`
- **THEN** o algoritmo não rotaciona a peça em 90 graus durante o encaixe na chapa

### Requirement: Exportação de Modelo 3D de Projeto
O servidor MCP SHALL expor uma ferramenta `export_3d_project` que recebe o tipo de móvel ou lista de peças e gera o arquivo de dados JSON da cena 3D compatível com o visualizador.

#### Scenario: Geração de modelo para armário ou cadeira
- **WHEN** o cliente invoca `export_3d_project` para um projeto calculado
- **THEN** o servidor gera as coordenadas e vetores de explosão de cada peça e salva ou retorna o arquivo do projeto

### Requirement: Geração de Modelo 3D para Qualquer Móvel do Chat
O servidor MCP SHALL expor uma ferramenta `preview_furniture_3d` capaz de gerar a cena 3D e atualizar `viewer/current_project.js` para qualquer tipo de móvel (armários com portas/gavetas, estantes, mesas, nichos ou cadeira krat).

#### Scenario: Geração dinâmica de móvel no chat
- **WHEN** o agente invoca `preview_furniture_3d` para um móvel solicitado pelo usuário
- **THEN** o arquivo `viewer/current_project.js` é atualizado com as peças, medidas e direções de explosão calculadas

