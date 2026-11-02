## Context

O usuário identificou falhas na geometria da Cadeira Krat (visíveis em `krat-error.png`) e solicitou que o visualizador 3D funcione de forma contínua para qualquer projeto que estiver sendo criado no chat.

## Goals / Non-Goals

**Goals:**
- **Correção da Cadeira Krat**:
  - Pés e braços montados em camadas reais: pernas verticais na camada interna ($X = \pm 250$ mm) e braços/travessas na camada externa ($X = \pm 268$ mm), eliminando z-fighting e cortes sobrepostos.
  - Adição dos dois suportes inclinados do assento (cleats de 95x18mm) que unem os pés dianteiros e traseiros na inclinação correta (~10°).
  - Adição dos dois montantes verticais/inclinados de apoio do encosto que sustentam firmemente as ripas horizontais sem flutuação.
- **Sincronização Dinâmica com o Chat**:
  - Salvar `viewer/current_project.js` contendo `window.CURRENT_PROJECT = { ... }` sempre que um projeto for discutido ou detalhado no chat.
  - Carregar esse arquivo via tag `<script>` em `viewer/index.html`, garantindo funcionamento instantâneo mesmo quando aberto via `file://` (sem restrições de CORS locais).
  - O visualizador detecta a presença de `CURRENT_PROJECT` e o seleciona como padrão na inicialização com a etiqueta `"🌟 Projeto Atual do Chat"`.
- **Geradores 3D Universais**:
  - Capacidade em Python de construir caixas, divisórias, prateleiras, gavetas e pés para qualquer móvel solicitado (armários, gabinetes, estantes, mesas, nichos).

**Non-Goals:**
- Servidor WebSocket permanente complexo. A escrita de `current_project.js` + botão de atualização/recarregamento no visualizador atende com máxima simplicidade e estabilidade offline.

## Decisions

1. **Abordagem de Transporte: JavaScript Global (`current_project.js`) vs Fetch API**
   - *Decisão*: Gravar o projeto em `viewer/current_project.js` com atribuição a `window.CURRENT_PROJECT`.
   - *Justificativa*: Em Windows ao abrir `viewer/index.html` com duplo clique (`file:///...`), a API `fetch()` é bloqueada pelo Chrome e Edge por segurança de mesma origem (`null origin`). Uma tag `<script src="current_project.js">` funciona 100% livre de bloqueios.

2. **Geometria Autêntica da Cadeira Krat**
   - *Decisão*: Reconstruir a estrutura completa baseada na marcenaria de Rietveld (17 peças no total: 4 pernas, 2 braços, 2 travessas inferiores, 2 suportes do assento, 4 ripas de assento, 2 montantes de encosto, 3 ripas de encosto).
