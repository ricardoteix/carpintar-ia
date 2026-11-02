# visualizador-3d-app Specification

## Purpose
Visualizador 3D interativo baseado em Three.js para renderização de móveis, visão explodida, inspeção de peças de marcenaria, guia de ferramentas e manual de montagem passo a passo com exportação.

## Requirements
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

### Requirement: Sincronização Automática com o Projeto do Chat
A aplicação web SHALL carregar automaticamente `current_project.js` na inicialização e selecionar o projeto gerado no chat como o modelo ativo principal.

#### Scenario: Abertura direta do visualizador
- **WHEN** o usuário abre ou recarrega `viewer/index.html` após gerar um projeto no chat
- **THEN** o projeto gerado no chat é exibido imediatamente em 3D com título, peças e visão explodida

### Requirement: Modelo Fiel da Cadeira Krat
A aplicação web SHALL renderizar a Cadeira Krat com 18 peças de 20mm divididas em 4 módulos construtivos alinhados aos dados do modelo DAE e manual oficial.

#### Scenario: Inspeção do modelo da Cadeira Krat
- **WHEN** a Cadeira Krat é selecionada
- **THEN** todas as ripas do encosto e assento repousam sobre suportes de madeira conectados à estrutura lateral sem peças flutuando

### Requirement: Modal de Manual de Montagem e Guia de Ferramentas
A aplicação web SHALL exibir um modal dedicado contendo a lista categorizada de ferramentas necessárias (essenciais, opcionais, EPIs) e o manual de montagem sequencial em fases e passos com checkboxes de progresso.

#### Scenario: Abertura do manual de montagem
- **WHEN** o usuário clica no botão "Manual"
- **THEN** uma janela modal exibe as ferramentas recomendadas e as etapas de montagem estruturadas

### Requirement: Exportação do Manual em Markdown (.md)
A aplicação web SHALL permitir o download imediato do manual de montagem em arquivo com extensão `.md` gerado no navegador.

#### Scenario: Download de arquivo Markdown
- **WHEN** o usuário clica em "Baixar .MD"
- **THEN** o navegador realiza o download do arquivo de texto formatado

### Requirement: Exportação do Manual em PDF / Impressão
A aplicação web SHALL fornecer folha de estilo de impressão otimizada (`@media print`) para geração limpa de PDF via diálogo nativo de impressão.

#### Scenario: Impressão do manual
- **WHEN** o usuário clica em "PDF / Imprimir"
- **THEN** o diálogo de impressão é acionado exibindo apenas o manual limpo formatado para páginas A4
