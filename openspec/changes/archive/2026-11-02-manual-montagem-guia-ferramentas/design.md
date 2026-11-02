# Design Técnico: Manual de Montagem, Guia de Ferramentas e Exportação PDF/MD

## Arquitetura Geral

```
┌────────────────────────────────────────────────────────────────┐
│ 1. MCP Server (Python)                                         │
│    • rules.py: dedução de ferramentas essenciais, opcionais e  │
│      EPIs baseadas no móvel (dobradiças -> caneco 35mm, etc.)  │
│    • project_3d.py: geração de assembly_guide (fases e passos) │
│    • server.py: nova tool generate_assembly_manual             │
└───────────────────────────────┬────────────────────────────────┘
                                │
                                ▼ Sincroniza via current_project.js
┌────────────────────────────────────────────────────────────────┐
│ 2. Visualizador Web 3D (HTML/CSS/JS)                           │
│    • Botão "📖 Manual de Montagem" na barra superior           │
│    • Modal/Painel deslizante exibindo:                         │
│      - 🧰 Lista de Ferramentas e EPIs                          │
│      - 📋 Fases e Passos sequenciais de montagem               │
│      - 📥 Botão "Baixar .MD" (Blob/Data URI no navegador)      │
│      - 🖨️ Botão "PDF / Imprimir" (window.print + @media print)  │
└────────────────────────────────────────────────────────────────┘
```

## 1. Estrutura de Dados do Manual (`assembly_guide`)

O objeto de projeto incluirá:
```json
{
  "title": "Cadeira Krat (Gerrit Rietveld, 1934)",
  "dimensions": "590 x 630 x 686 mm",
  "tools": {
    "essential": [
      { "name": "Parafusadeira / Furadeira", "spec": "Controle de torque" },
      { "name": "Broca Piloto com Escareador", "spec": "3mm (para parafusos 4.0mm)" },
      { "name": "Bit Phillips PH2", "spec": "Ponteira magnética" },
      { "name": "Grampos Sargentos", "spec": "Tipo F ou 90° (ao menos 2 a 4)" },
      { "name": "Esquadro e Trena", "spec": "Metálicos para medição precisa" }
    ],
    "optional": [
      { "name": "Lixa Grão 150/220", "spec": "Quebra de cantos e rebarbas" },
      { "name": "Gabarito de Cavilha/Minifix", "spec": "Se optar por junção invisível" }
    ],
    "safety": [
      "Óculos de proteção",
      "Máscara contra poeira de madeira/MDF (PFF2)"
    ]
  },
  "assembly_guide": {
    "estimated_time_hours": 2.5,
    "difficulty": "Médio",
    "phases": [
      {
        "phase_number": 1,
        "title": "Conferência e Pré-Furação",
        "steps": [
          "Confira todas as peças conforme a lista de corte (BOM).",
          "Marque os pontos de furação com lápis e esquadro.",
          "Faça furações piloto com broca 3mm escareando a face externa."
        ]
      },
      {
        "phase_number": 2,
        "title": "Montagem dos Módulos Laterais",
        "steps": [
          "Una os pés dianteiro e traseiro à travessa larga com grampos.",
          "Fixe o apoio de braço no topo garantindo alinhamento frontal."
        ]
      }
    ]
  }
}
```

## 2. Exportação no Visualizador

### Exportação Markdown (`.md`)
- Função cliente pura em JavaScript:
  ```javascript
  const blob = new Blob([markdownContent], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `manual_montagem_${slug}.md`;
  a.click();
  ```

### Exportação PDF / Impressão
- CSS com `@media print`:
  - Oculta o canvas WebGL 3D, barras de ferramentas, botões e controles laterais.
  - Exibe o manual formatado em preto e branco / cores limpas em folha A4 com quebras de página controladas (`page-break-inside: avoid`).
  - Acionado via `window.print()`.
