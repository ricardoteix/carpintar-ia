# mcp-server-leomadeiras Specification Delta

## Added Requirements

### Requirement: Dedução de Ferramentas e Insumos de Montagem
O servidor MCP SHALL deduzir a lista de ferramentas essenciais, opcionais e EPIs de acordo com a complexidade estrutural e ferragens do móvel.

#### Scenario: Dedução de ferramentas para armário com portas
- **WHEN** o móvel possui dobradiças tipo caneco de 35mm
- **THEN** a lista de ferramentas inclui broca forstner/caneco de 35mm, parafusadeira e broca piloto de 3mm

### Requirement: Ferramenta de Geração de Manual de Montagem
O servidor MCP SHALL expor a ferramenta `generate_assembly_manual` que retorna o passo a passo em texto estruturado e o inclui no projeto 3D exportado.

#### Scenario: Chamada da ferramenta de manual
- **WHEN** o cliente MCP chama `generate_assembly_manual(furniture_type="krat")`
- **THEN** o retorno contém as fases lógicas de pré-montagem, montagem estrutural e acabamento
