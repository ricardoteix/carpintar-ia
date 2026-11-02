## ADDED Requirements

### Requirement: Sincronização Automática com o Projeto do Chat
A aplicação web SHALL carregar automaticamente `current_project.js` na inicialização e selecionar o projeto gerado no chat como o modelo ativo principal.

#### Scenario: Abertura direta do visualizador
- **WHEN** o usuário abre ou recarrega `viewer/index.html` após gerar um projeto no chat
- **THEN** o projeto gerado no chat é exibido imediatamente em 3D com título, peças e visão explodida

### Requirement: Modelo Fiel da Cadeira Krat
A aplicação web SHALL renderizar a Cadeira Krat com suporte estrutural completo, montantes de encosto e encaixes em camadas sem sobreposição de volumes.

#### Scenario: Inspeção do modelo da Cadeira Krat
- **WHEN** a Cadeira Krat é selecionada
- **THEN** todas as ripas do encosto e assento repousam sobre suportes de madeira conectados à estrutura lateral
