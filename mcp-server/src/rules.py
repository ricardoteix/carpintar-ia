"""Regras e utilitários de marcenaria para cálculo de kits de ferragens e insumos."""

from typing import Any, Dict, List, Optional
import math


def calculate_hinges_count(door_height_mm: float) -> int:
    """Calcula a quantidade recomendada de dobradiças caneco 35mm por porta com base na altura."""
    if door_height_mm <= 900:
        return 2
    elif door_height_mm <= 1600:
        return 3
    elif door_height_mm <= 2000:
        return 4
    else:
        return 5


def recommend_hardware(
    furniture_type: str,
    pieces_count: int = 4,
    doors: int = 0,
    door_height_mm: float = 600.0,
    drawers: int = 0,
    linear_edge_meters: Optional[float] = None,
    sheet_thickness_mm: int = 15,
) -> Dict[str, Any]:
    """Calcula a lista recomendada de insumos e ferragens para montagem de móvel.

    Args:
        furniture_type: Tipo do móvel (ex: 'nicho', 'armario', 'gaveteiro', 'bancada', 'prateleira')
        pieces_count: Quantidade total estimada de peças de corte da caixaria
        doors: Quantidade de portas
        door_height_mm: Altura média das portas em milímetros
        drawers: Quantidade de gavetas
        linear_edge_meters: Metragem estimada de fita de borda (opcional)
        sheet_thickness_mm: Espessura predominante do MDF (ex: 15 ou 18mm)
    """
    items: List[Dict[str, Any]] = []

    # 1. Parafusos estruturais de caixaria (junção de topos)
    # Estima-se 4 parafusos por peça montada (2 em cada extremidade)
    structural_screws_count = max(8, pieces_count * 4)
    screw_size = "4.0 x 40 mm" if sheet_thickness_mm <= 15 else "4.0 x 50 mm"
    items.append({
        "category": "Fixação Estrutural",
        "item": f"Parafuso Chipboard Cabeça Chata {screw_size}",
        "suggested_quantity": structural_screws_count,
        "unit": "unidades",
        "search_term": f"Parafuso Chipboard {screw_size}",
        "notes": "Para junção das peças de caixaria (furo guia com broca 3mm recomendado).",
    })

    # Tapa-furos adesivos para parafusos externos
    items.append({
        "category": "Acabamento",
        "item": "Cartela de Tapa-furo Adesivo (12mm)",
        "suggested_quantity": math.ceil(structural_screws_count / 20),
        "unit": "cartela(s)",
        "search_term": "Tapa Furo Adesivo",
        "notes": "Na mesma tonalidade/textura do MDF escolhido.",
    })

    # 2. Dobradiças para portas
    if doors > 0:
        hinges_per_door = calculate_hinges_count(door_height_mm)
        total_hinges = doors * hinges_per_door
        items.append({
            "category": "Ferragens de Abertura",
            "item": "Dobradiça de Pressão Caneco 35mm Reta com Amortecedor (Soft Close)",
            "suggested_quantity": total_hinges,
            "unit": "unidades",
            "search_term": "Dobradiça Caneco 35mm Amortecedor Reta",
            "notes": f"{hinges_per_door} dobradiças por porta para altura de {door_height_mm}mm.",
        })
        # Parafusos para fixar as dobradiças (4 por dobradiça: 2 no calço, 2 no caneco)
        items.append({
            "category": "Fixação de Ferragens",
            "item": "Parafuso Chipboard Cabeça Chata 3.5 x 16 mm",
            "suggested_quantity": total_hinges * 4,
            "unit": "unidades",
            "search_term": "Parafuso Chipboard 3.5x16mm",
            "notes": "Para fixação das dobradiças no MDF sem estufar a chapa.",
        })

    # 3. Corrediças para gavetas
    if drawers > 0:
        items.append({
            "category": "Ferragens de Deslizamento",
            "item": "Par de Corrediças Telescópicas Reforçadas (ex: 400mm ou 450mm)",
            "suggested_quantity": drawers,
            "unit": "par(es)",
            "search_term": "Corrediça Telescópica 450mm",
            "notes": "Escolher a profundidade conforme a profundidade livre da caixaria.",
        })
        # Parafusos para corrediças (8 parafusos 3.5x16 por gaveta)
        items.append({
            "category": "Fixação de Ferragens",
            "item": "Parafuso Chipboard Cabeça Chata 3.5 x 16 mm",
            "suggested_quantity": drawers * 8,
            "unit": "unidades",
            "search_term": "Parafuso Chipboard 3.5x16mm",
            "notes": "Para fixação dos trilhos das corrediças.",
        })

    # 4. Fita de Borda e Colagem
    if linear_edge_meters is not None and linear_edge_meters > 0:
        # Adicionar 15% de margem de segurança para refile e cantos
        safe_edge_meters = round(linear_edge_meters * 1.15, 1)
        edge_width = "22 mm" if sheet_thickness_mm <= 18 else "35 mm"
        items.append({
            "category": "Borda e Fita",
            "item": f"Fita de Borda PVC {edge_width} x 0,45mm",
            "suggested_quantity": safe_edge_meters,
            "unit": "metros lineares",
            "search_term": f"Fita de Borda {edge_width}",
            "notes": f"Calculado {linear_edge_meters}m com margem de 15% para refile.",
        })
        items.append({
            "category": "Químicos e Colas",
            "item": "Cola de Contato para Fita de Borda ou Adesivo Instantâneo com Ativador",
            "suggested_quantity": 1,
            "unit": "tubo/lata",
            "search_term": "Cola de Contato Marcenaria",
            "notes": "Para colagem manual da fita de borda nas extremidades usinadas.",
        })

    # 5. Fixação na parede (se for nicho, prateleira ou aéreo)
    f_type_lower = furniture_type.lower()
    if any(k in f_type_lower for k in ["nicho", "aereo", "aéreo", "parede", "prateleira", "painel"]):
        items.append({
            "category": "Fixação na Parede",
            "item": "Suporte Cantoneira de Aço 2 Furos com Capa Plástica + Buchas 8mm",
            "suggested_quantity": 4,
            "unit": "conjuntos",
            "search_term": "Cantoneira 2 furos capa plastica",
            "notes": "Para fixação oculta e reforçada na parede.",
        })

    return {
        "furniture_type": furniture_type,
        "sheet_thickness_mm": sheet_thickness_mm,
        "total_items_recommended": len(items),
        "hardware_kit": items,
    }

def recommend_tools(
    furniture_type: str,
    doors: int = 0,
    drawers: int = 0,
    cuts_in_shop: bool = False,
) -> Dict[str, Any]:
    """Deduz o conjunto estruturado de ferramentas essenciais, opcionais e EPIs para montagem do móvel.

    Args:
        furniture_type: Tipo do móvel ('krat', 'armario', 'nicho', 'estante', etc.)
        doors: Quantidade de portas (para dobradiças 35mm)
        drawers: Quantidade de gavetas (para corrediças)
        cuts_in_shop: Se o marceneiro fará os cortes e fitamento na própria oficina
    """
    f_type = furniture_type.lower()
    is_wood_solid = "krat" in f_type or "madeira" in f_type or "pinus" in f_type

    essential: List[Dict[str, str]] = [
        {
            "name": "Parafusadeira / Furadeira",
            "spec": "Mandril de 3/8 pol com controle de torque (evita espanar MDF ou trincar madeira)",
            "why": "Furação piloto rápida e parafusamento firme com torque regulado.",
        },
        {
            "name": "Broca Piloto 3.0 mm com Escareador",
            "spec": "Broca de aço rápido 3mm + escareador 45°",
            "why": "A furação piloto evita que o MDF estufe ou o Pinus rache no topo; o escareador embutir a cabeça do parafuso.",
        },
        {
            "name": "Bit Phillips PH2",
            "spec": "Ponteira de impacto de 50mm ou 65mm com retenção magnética",
            "why": "Encaixe preciso nos parafusos chipboard sem estragar a fenda.",
        },
        {
            "name": "Trena Metálica e Lápis de Marceneiro",
            "spec": "Trena de 3m a 5m com trava + lápis rígido (grau 2H ou carpinteiro)",
            "why": "Medição de diagonais e marcação exata das linhas de furação.",
        },
        {
            "name": "Esquadro Combinado Metálico",
            "spec": "300mm com escala milimétrica e bolha de nível",
            "why": "Garantir 90° perfeitos nos encontros de topos e marcações paralelas.",
        },
        {
            "name": "Grampos Sargentos (2 a 4 unidades)",
            "spec": "Grampos tipo F (abertura 300mm) ou grampos angulares 90°",
            "why": "Seguram as peças firmemente unidas durante a furação e parafusamento, impedindo desalinhamento.",
        },
    ]

    # Ferramenta para portas (se houver dobradiça caneco 35mm e não vier furado da loja)
    if doors > 0:
        essential.append({
            "name": "Broca Forstner / Fresa Caneco 35 mm",
            "spec": "Fresa Forstner 35mm com ponta de centro (ou gabarito de caneco)",
            "why": "Usinagem da cavidade de 11.5mm de profundidade na face interna das portas para instalar as dobradiças.",
        })

    # Ferramenta para gavetas
    if drawers > 0:
        essential.append({
            "name": "Nível de Mão e Régua Metálica",
            "spec": "Nível bolha de 30cm a 40cm",
            "why": "Garantir que os pares de corrediças fiquem 100% nivelados e paralelos em ambos os lados.",
        })

    optional: List[Dict[str, str]] = [
        {
            "name": "Bloco com Lixa Grão 150 / 220",
            "spec": "Lixa para madeira ou esponja abrasiva média/fina",
            "why": "Quebra suave de cantos vivos ('arrebitas') e remoção de marcas de lápis.",
        },
        {
            "name": "Gabarito de Furação de Cavilhas / Minifix",
            "spec": "Gabarito autocentrante para furos de 6mm e 8mm",
            "why": "Permite conexões invisíveis sem parafusos aparentes nas laterais externas.",
        },
    ]

    if cuts_in_shop:
        optional.extend([
            {
                "name": "Serra Circular Manual com Trilho Guia",
                "spec": "Disco para MDF com 60 dentes trapezoidais (dentes ED)",
                "why": "Corte de chapas retas sem lascar o revestimento melamínico.",
            },
            {
                "name": "Refilador de Fita de Borda e Estilete",
                "spec": "Refilador duplo de facas intercambiáveis + estilete trapezoidal",
                "why": "Corte do excesso de fita de borda rente à chapa sem riscar o MDF.",
            },
            {
                "name": "Soprador Térmico ou Ferro de Passar",
                "spec": "Controle de temperatura ~150°C a 200°C",
                "why": "Aplicação de fita de borda pré-encolada ou amolecimento de cola de contato.",
            },
        ])

    safety: List[Dict[str, str]] = [
        {
            "item": "Óculos de Proteção",
            "reason": "Protege contra cavacos e farpas projetadas na furação e corte.",
        },
        {
            "item": "Máscara de Proteção Respiratória (PFF2)",
            "reason": "O pó fino de MDF contém resinas e formaldeído; use sempre ao furar ou lixar.",
        },
        {
            "item": "Protetor Auricular (Plug ou Concha)",
            "reason": "Proteção auditiva ao operar ferramentas elétricas (furadeiras, serras).",
        },
    ]

    return {
        "furniture_type": furniture_type,
        "is_wood_solid": is_wood_solid,
        "cuts_in_shop": cuts_in_shop,
        "essential_tools": essential,
        "optional_tools": optional,
        "safety_equipment": safety,
    }

