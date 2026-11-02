## ADDED Requirements

### Requirement: Exportação de Modelo 3D de Projeto
O servidor MCP SHALL expor uma ferramenta `export_3d_project` que recebe o tipo de móvel ou lista de peças e gera o arquivo de dados JSON da cena 3D compatível com o visualizador.

#### Scenario: Geração de modelo para armário ou cadeira
- **WHEN** o cliente invoca `export_3d_project` para um projeto calculado
- **THEN** o servidor gera as coordenadas e vetores de explosão de cada peça e salva ou retorna o arquivo do projeto
