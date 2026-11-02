## ADDED Requirements

### Requirement: Otimização de Plano de Corte 2D
O servidor MCP SHALL expor uma ferramenta `calculate_cutting_plan` que recebe uma lista de peças com dimensões e quantidades e calcula a quantidade mínima de chapas necessárias, considerando folga de serra (*kerf*) e margem de refile.

#### Scenario: Cálculo de corte com chapa padrão de MDF
- **WHEN** o cliente invoca `calculate_cutting_plan` com peças de um móvel e dimensões de chapa (2750 x 1830 mm)
- **THEN** o servidor retorna o total de chapas necessárias, percentual de aproveitamento e disposição das peças por chapa

#### Scenario: Respeito à orientação de veio
- **WHEN** uma peça possui o parâmetro `can_rotate=False`
- **THEN** o algoritmo não rotaciona a peça em 90 graus durante o encaixe na chapa
