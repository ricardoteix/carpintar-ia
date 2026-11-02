## Context

O visualizador 3D precisa ser instantâneo, leve e acessível localmente sem exigir servidores Node.js em execução contínua ou processos pesados de compilação/bundling. Deve rodar diretamente em qualquer navegador moderno (Chrome, Edge, Firefox) abrindo o arquivo `viewer/index.html` ou através do MCP Server.

## Goals / Non-Goals

**Goals:**
- Criar aplicação frontend limpa em `viewer/` (HTML5, Vanilla JavaScript moderno com ES Modules e Three.js via CDN/local).
- Implementar controle de câmera tipo órbita (rotacionar, aproximar/afastar zoom, transladar).
- Implementar slider interativo de **Visão Explodida**:
  - Cada peça possui uma posição central original $(x_0, y_0, z_0)$ e um vetor de explosão normalizado $(dx, dy, dz)$.
  - Quando o slider varia de $0$ a $1$, a posição da peça interpola suavemente para $(x_0 + dx \cdot \text{fator}, y_0 + dy \cdot \text{fator}, z_0 + dz \cdot \text{fator})$.
- Tooltips e painel lateral com detalhes da peça selecionada (nome, dimensões C x L x E em mm e material).
- Seletor de acabamento: MDF Branco Texturizado vs Madeira Pinus Natural com veios.
- Presets prontos para carregar com 1 clique:
  1. Cadeira Krat clássica de Rietveld
  2. Armário Aéreo de 2 Portas
  3. Nicho Retangular de Parede
- Ferramenta MCP `export_3d_project` para salvar projetos customizados em `viewer/projects/` ou gerar HTML direto.

**Non-Goals:**
- Software CAD completo com edição paramétrica de malha geométrica. O foco é visualização, montagem e validação explodida.

## Decisions

1. **Frontend Standalone (ES Modules + Three.js)**
   - *Decisão*: Utilizar HTML5 puro com Three.js carregado via ESM (`import * as THREE from 'three'`).
   - *Justificativa*: Abre com duplo clique no arquivo local sem precisar rodar `npm install` ou servidores complexos, garantindo portabilidade máxima.

2. **Modelo de Dados de Peça 3D**
   - Cada peça é representada por:
     `{ id, name, dimensions: [length, width, thickness], position: [x, y, z], rotation: [rx, ry, rz], explode_direction: [dx, dy, dz] }`
   - O algoritmo calcula os vetores de explosão automaticamente a partir do centroide do móvel, facilitando a montagem de qualquer projeto futuro.
