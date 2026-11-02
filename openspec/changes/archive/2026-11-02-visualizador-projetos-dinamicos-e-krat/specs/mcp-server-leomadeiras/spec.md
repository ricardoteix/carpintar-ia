## ADDED Requirements

### Requirement: Geração de Modelo 3D para Qualquer Móvel do Chat
O servidor MCP SHALL expor uma ferramenta `preview_furniture_3d` capaz de gerar a cena 3D e atualizar `viewer/current_project.js` para qualquer tipo de móvel (armários com portas/gavetas, estantes, mesas, nichos ou cadeira krat).

#### Scenario: Geração dinâmica de móvel no chat
- **WHEN** o agente invoca `preview_furniture_3d` para um móvel solicitado pelo usuário
- **THEN** o arquivo `viewer/current_project.js` é atualizado com as peças, medidas e direções de explosão calculadas
