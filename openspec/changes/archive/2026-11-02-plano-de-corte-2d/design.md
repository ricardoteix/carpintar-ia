## Context

Marcenaria moderna de chapas baseia-se em otimizar cortes lineares contínuos (cortes de guilhotina executados em seccionadoras ou esquadrejadeiras). A ferramenta de plano de corte precisa receber uma lista de peças com largura, comprimento e quantidade, e distribuir nas chapas considerando a espessura da serra (*kerf*) e as perdas de refile.

## Goals / Non-Goals

**Goals:**
- Implementar algoritmo 2D Guillotine Bin Packing / Shelf First-Fit Decreasing em Python puro, sem dependências pesadas de C++.
- Considerar dimensões padrão da chapa brasileira de MDF (2750 x 1830 mm), personalizável para outras medidas (ex: compensado 2200 x 1600 mm ou painel de pinus 2400 x 300 mm).
- Tratar *kerf* da lâmina de corte (padrão 4mm) e margem perimetral de refile (padrão 10mm).
- Suportar restrição de sentido de veio (*grain direction / allow_rotation*).
- Retornar resumo detalhado: quantidade de chapas, porcentagem de aproveitamento de área (área útil das peças vs área total da chapa), peças por chapa e lista de sobras/retalhos aproveitáveis.

**Non-Goals:**
- Nesting não ortogonal (peças curvas em CNC router). O foco é corte reto de esquadrejadeira/seccionadora.
- Exportação direta de arquivo G-Code proprietário nesta fase.

## Decisions

1. **Algoritmo: Guillotine Cut Best-Fit / First-Fit Decreasing**
   - *Decisão*: Implementar particionamento retangular ortogonal (Guillotine splits). Quando uma peça é encaixada num retângulo livre, o espaço restante é dividido em dois novos retângulos livres (um horizontal e um vertical).
   - *Justificativa*: Garante que todo corte é factível em uma esquadrejadeira física de marcenaria (corte de ponta a ponta sem recortes em L que travam a lâmina).

2. **Formato dos Dados de Entrada e Saída**
   - Entrada: Lista de dicionários `[{"name": "Lateral", "length": 600, "width": 350, "quantity": 2, "can_rotate": True}]`.
   - Saída: `{"sheets_needed": 1, "utilization_percent": 78.4, "sheets": [...], "offcuts": [...]}`.

## Risks / Trade-offs

- **[Risco] Problema NP-Hard de Bin Packing** → *Mitigação*: Heurística gulosa ordenada por maior área/comprimento (FFD/BFD) encontra soluções ótimas ou próximas do ótimo em milissegundos para projetos típicos residenciais (10 a 80 peças).
