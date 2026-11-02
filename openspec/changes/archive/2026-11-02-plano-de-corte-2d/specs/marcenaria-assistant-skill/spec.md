## ADDED Requirements

### Requirement: Estimativa e Apresentação de Plano de Corte
A Skill SHALL orientar o agente a sugerir e calcular o plano de corte das peças através da ferramenta `calculate_cutting_plan`, informando quantas chapas completas o cliente precisa adquirir na Leo Madeiras.

#### Scenario: Projeto com consumo de chapas
- **WHEN** a lista de peças (BOM) for concluída
- **THEN** o agente calcula a estimativa de chapas de MDF necessárias e informa o percentual de aproveitamento e sobras
