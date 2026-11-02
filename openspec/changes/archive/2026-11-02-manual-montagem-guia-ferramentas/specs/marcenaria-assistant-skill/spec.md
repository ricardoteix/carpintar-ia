# marcenaria-assistant-skill Specification Delta

## Added Requirements

### Requirement: Orientação de Ferramentas e Segurança
A skill SHALL instruir o usuário sobre o ferramental mínimo obrigatório e equipamentos de proteção individual (EPIs) antes do início da montagem.

#### Scenario: Orientação do assistente no chat
- **WHEN** um projeto de móvel é finalizado
- **THEN** o assistente apresenta o resumo das ferramentas necessárias e oferece o manual de montagem

### Requirement: Entrega do Manual Passo a Passo
A skill SHALL orientar o usuário a inspecionar e baixar o manual de montagem diretamente no visualizador 3D ou consultar no próprio chat.

#### Scenario: Consulta do manual
- **WHEN** o usuário solicita instruções de montagem
- **THEN** o assistente apresenta a sequência ordenada de fases com tempos estimados e cuidados de esquadro
