## ADDED Requirements

### Requirement: Renderização de Móveis 3D e Navegação
A aplicação web SHALL renderizar as peças do móvel no espaço tridimensional com materiais visuais realistas (Pinus e MDF Branco) e permitir rotação, pan e zoom por meio de OrbitControls.

#### Scenario: Carga e inspeção de modelo 3D
- **WHEN** o usuário abre a aplicação web no navegador
- **THEN** o móvel é renderizado centralizado com iluminação ambiente e sombras suaves

### Requirement: Controle Deslizante de Visão Explodida
A aplicação SHALL conter um controle deslizante (slider de 0% a 100%) que separa dinamicamente as peças em seus respectivos eixos de montagem.

#### Scenario: Interação com o slider de explosão
- **WHEN** o usuário arrasta o controle para 50%
- **THEN** as peças se afastam proporcionalmente ao longo dos vetores de montagem sem perder a orientação original

### Requirement: Painel de Informações da Peça
A aplicação SHALL exibir nome, dimensões (comprimento, largura, espessura em mm) e função da peça quando o usuário clicar ou passar o cursor sobre ela.

#### Scenario: Seleção de peça
- **WHEN** o usuário clica sobre uma lateral ou porta no modelo 3D
- **THEN** a peça recebe destaque visual e o painel exibe suas medidas detalhadas
