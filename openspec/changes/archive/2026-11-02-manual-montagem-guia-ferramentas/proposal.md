# Proposta: Manual de Montagem Estruturado, Guia de Ferramentas e Exportação (PDF/MD)

## Por que?
Atualmente, o assistente de marcenaria gera listas de corte (BOM), planos de corte 2D otimizados, kits de ferragens e visualização 3D com visão explodida. No entanto, para que o usuário (seja hobbysta DIY ou profissional) consiga executar o projeto na prática, ainda faltam duas etapas cruciais:
1. **Guia de Ferramentas e EPIs**: Informar com clareza quais ferramentas são obrigatórias para executar a furação, montagem e acabamento daquele móvel específico (diferenciando quem recebe peças já cortadas da madeireira de quem vai cortar na própria oficina).
2. **Manual de Montagem Passo a Passo**: Um roteiro sequencial estruturado por fases lógicas (conferência, pré-furações, pré-montagem de módulos, montagem do corpo, fixação de fundo e regulagens finas), integrado diretamente no visualizador 3D com opções de download em Markdown (.md) ou impressão/PDF.

## O que será feito?
1. **Modelagem de Ferramentas e Instruções no Servidor MCP (`project_3d.py` e `rules.py`)**:
   - Algoritmo que deduz as ferramentas necessárias de acordo com o tipo de móvel (ex: furadeira, broca escareadora 3mm, broca caneco 35mm para dobradiças, grampos sargentos, nível, esquadro).
   - Gerador do roteiro de montagem detalhado passo a passo (com tempos estimados, avisos de esquadro, torque e dicas de segurança).
   - Inclusão do objeto `assembly_guide` e `tools_required` dentro da estrutura do projeto salvo (`current_project.js`, `current_project.json` e arquivo arquivado em `projects/`).
2. **Nova Ferramenta MCP `generate_assembly_manual`**:
   - Permite que o agente consulte ou gere o manual em texto markdown diretamente no chat ou salve no visualizador.
3. **Interface do Manual no Visualizador 3D (`viewer/index.html` e `viewer/app.js`)**:
   - Botão e aba/modal interativa `📖 Manual de Montagem` na barra superior ou painel lateral.
   - Renderização limpa dos passos de montagem com checkboxes de progresso.
   - Botão **`📥 Baixar .MD`**: download do manual completo em Markdown.
   - Botão **`🖨️ Imprimir / Salvar PDF`**: acionamento do fluxo de impressão nativo com folha de estilo CSS print-friendly (sem interface de botões, formatado para A4).
4. **Atualização da Skill `marcenaria-assistant`**:
   - Inclusão da etapa de apresentação das ferramentas necessárias e oferta proativa do manual de montagem.

## Não-Escopo
- Não inclui geração de vídeo ou animação procedural passo a passo da montagem em vídeo (o slider 3D de visão explodida e o manual em texto/diagramas cobrem essa necessidade).
- Não requer dependências externas pesadas de backend para gerar PDF (será utilizado o motor de impressão nativo do navegador com `@media print` otimizado para salvar em PDF com zero latência e sem dependências extras).
