## ADDED Requirements

### Requirement: Atualização Automática do Visualizador em Projetos
A Skill SHALL orientar o agente a sempre acionar a ferramenta `preview_furniture_3d` ao detalhar um móvel no chat, informando ao usuário que o visualizador já está atualizado.

#### Scenario: Conclusão do projeto no chat
- **WHEN** o agente finaliza o cálculo da lista de corte e orçamento
- **THEN** o agente atualiza o modelo 3D e avisa que o visualizador já reflete o projeto atual
