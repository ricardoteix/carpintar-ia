# marcenaria-assistant-skill Specification

## Purpose
TBD - created by archiving change leomadeiras-marcenaria-mcp-skill. Update Purpose after archive.
## Requirements
### Requirement: Orientação e Decomposição de Móveis em Peças
A Skill SHALL fornecer ao agente instruções para decompor a solicitação de um móvel em sua lista de corte (BOM), aplicando descontos de espessura de chapa (ex: 15mm ou 18mm) para tampos, bases, laterais e fundos.

#### Scenario: Decomposição de nicho retangular
- **WHEN** o usuário informa as medidas externas de largura, altura e profundidade de um nicho
- **THEN** o agente calcula as medidas de corte das peças descontando a espessura das chapas sobrepostas

### Requirement: Estimativa de Insumos Invisíveis
A Skill SHALL orientar o agente a calcular e sugerir os insumos de fixação e acabamento necessários para o móvel planejado (fita de borda, parafusos, cola, suportes).

#### Scenario: Inclusão de fita de borda e parafusos
- **WHEN** o plano de peças é definido
- **THEN** o agente estima a metragem linear de fita de borda para as faces visíveis e quantifica os parafusos adequados à espessura da chapa

### Requirement: Orçamentação via MCP
A Skill SHALL instruir o agente a acionar as ferramentas do MCP Server da Leo Madeiras para verificar preços e disponibilidade dos materiais selecionados.

#### Scenario: Cotação de materiais do projeto
- **WHEN** as peças e insumos forem identificados
- **THEN** o agente executa a busca no MCP para cotar as chapas de MDF, fitas de borda e ferragens, apresentando o custo estimado consolidado

### Requirement: Estimativa e Apresentação de Plano de Corte
A Skill SHALL orientar o agente a sugerir e calcular o plano de corte das peças através da ferramenta `calculate_cutting_plan`, informando quantas chapas completas o cliente precisa adquirir na Leo Madeiras.

#### Scenario: Projeto com consumo de chapas
- **WHEN** a lista de peças (BOM) for concluída
- **THEN** o agente calcula a estimativa de chapas de MDF necessárias e informa o percentual de aproveitamento e sobras

### Requirement: Disponibilização de Visualização 3D ao Usuário
A Skill SHALL instruir o agente a sugerir e fornecer a visualização 3D explodida do móvel, indicando o arquivo local `viewer/index.html` para inspeção visual do projeto.

#### Scenario: Orientação de montagem 3D
- **WHEN** o usuário conclui o detalhamento de um móvel
- **THEN** o agente informa como abrir a visualização 3D e usar o controle de visão explodida

### Requirement: Atualização Automática do Visualizador em Projetos
A Skill SHALL orientar o agente a sempre acionar a ferramenta `preview_furniture_3d` ao detalhar um móvel no chat, informando ao usuário que o visualizador já está atualizado.

#### Scenario: Conclusão do projeto no chat
- **WHEN** o agente finaliza o cálculo da lista de corte e orçamento
- **THEN** o agente atualiza o modelo 3D e avisa que o visualizador já reflete o projeto atual

