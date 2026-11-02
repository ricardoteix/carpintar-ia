# visualizador-3d-app Specification Delta

## Added Requirements

### Requirement: Modal de Manual de Montagem e Guia de Ferramentas
A aplicação web SHALL exibir um modal ou painel dedicado contendo a lista categorizada de ferramentas necessárias e o manual de montagem sequencial em fases e passos.

#### Scenario: Abertura do manual de montagem
- **WHEN** o usuário clica no botão "Manual de Montagem"
- **THEN** uma janela exibe as ferramentas essenciais, EPIs e as etapas de montagem detalhadas com checkboxes de progresso

### Requirement: Exportação do Manual em Markdown (.md)
A aplicação web SHALL permitir o download imediato do manual de montagem em arquivo com extensão `.md`.

#### Scenario: Download de arquivo Markdown
- **WHEN** o usuário clica em "Baixar .MD"
- **THEN** o navegador realiza o download do arquivo de texto formatado contendo lista de ferramentas e passos

### Requirement: Exportação do Manual em PDF / Impressão
A aplicação web SHALL fornecer folha de estilo de impressão otimizada (`@media print`) para geração de PDF sem elementos de interface gráfica.

#### Scenario: Impressão do manual
- **WHEN** o usuário clica em "Imprimir / PDF"
- **THEN** o diálogo de impressão do navegador é aberto exibindo apenas o manual limpo formatado para páginas A4
