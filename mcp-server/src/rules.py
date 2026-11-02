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
