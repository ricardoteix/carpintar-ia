## ADDED Requirements

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
