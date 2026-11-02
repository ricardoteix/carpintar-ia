try:
    from .rules import recommend_tools
except ImportError:
    try:
        from src.rules import recommend_tools
    except ImportError:
        from rules import recommend_tools

"""Gerador de dados 3D, cálculos paramétricos de móveis e exportador para o visualizador."""

from typing import Any, Dict, List, Optional
import json
import math
import os
import unicodedata
import re


def generate_krat_chair_3d() -> Dict[str, Any]:
    """Gera o modelo 3D oficial da Cadeira Krat (Gerrit Rietveld, 1934).
    
    Extraído com precisão milimétrica direta do modelo oficial Collada (krat-model.dae)
    e em estrita conformidade com o manual modular montagem-krat.md:
    - Total: exatamente 18 peças de espessura 20mm.
    - Módulo 0 (Lateral Esquerda): 4 peças (Braço, Travessa Larga, Pé Frontal, Pé Traseiro).
    - Módulo 1 (Lateral Direita): 4 peças (Braço, Travessa Larga, Pé Frontal, Pé Traseiro).
    - Módulo 2 (Assento): 5 peças (2 Travessas de Suporte de 490mm + 3 Tábuas de 450mm).
    - Módulo 3 (Encosto): 5 peças (3 Tábuas verticais de 445mm + 2 Travessas traseiras de 450mm).
    """
    pieces: List[Dict[str, Any]] = [
        {
            "id": "group_0_braco",
            "name": "Lateral Esquerda - Apoio de Braço",
            "group": "group_0",
            "groupLabel": "Lateral Esquerda",
            "size": [20.0, 70.0, 600.0],
            "pos": [-260.0, 460.0, 0.0],
            "rot": [-3.14159, -0.0, -1.5708],
            "quaternion": [0.70711, 0.70711, -0.0, -0.0],
            "dir": [-1.6, 0.0, 0.0],
            "dims": [20.0, 70.0, 600.0],
        },
        {
            "id": "group_0_travessa",
            "name": "Lateral Esquerda - Travessa Larga",
            "group": "group_0",
            "groupLabel": "Lateral Esquerda",
            "size": [20.0, 140.0, 600.0],
            "pos": [-255.0, 225.0, 0.0],
            "rot": [3.14159, -0.0, -0.0],
            "quaternion": [1.0, 0.0, -0.0, 0.0],
            "dir": [-1.6, 0.0, 0.0],
            "dims": [20.0, 140.0, 600.0],
        },
        {
            "id": "group_0_pe_frontal",
            "name": "Lateral Esquerda - Pé Frontal",
            "group": "group_0",
            "groupLabel": "Lateral Esquerda",
            "size": [20.0, 140.0, 450.0],
            "pos": [-275.0, 225.0, 230.0],
            "rot": [1.5708, 0.0, -0.0],
            "quaternion": [0.70711, 0.0, -0.0, 0.70711],
            "dir": [-1.6, 0.0, 0.0],
            "dims": [20.0, 140.0, 450.0],
        },
        {
            "id": "group_0_pe_traseiro",
            "name": "Lateral Esquerda - Pé Traseiro",
            "group": "group_0",
            "groupLabel": "Lateral Esquerda",
            "size": [20.0, 140.0, 450.0],
            "pos": [-235.0, 225.0, -230.0],
            "rot": [1.5708, 0.0, -0.0],
            "quaternion": [0.70711, 0.0, -0.0, 0.70711],
            "dir": [-1.6, 0.0, 0.0],
            "dims": [20.0, 140.0, 450.0],
        },
        {
            "id": "group_1_braco",
            "name": "Lateral Direita - Apoio de Braço",
            "group": "group_1",
            "groupLabel": "Lateral Direita",
            "size": [20.0, 70.0, 600.0],
            "pos": [260.0, 460.0, 0.0],
            "rot": [0.0, 0.0, 1.5708],
            "quaternion": [0.0, 0.0, 0.70711, 0.70711],
            "dir": [1.6, 0.0, 0.0],
            "dims": [20.0, 70.0, 600.0],
        },
        {
            "id": "group_1_travessa",
            "name": "Lateral Direita - Travessa Larga",
            "group": "group_1",
            "groupLabel": "Lateral Direita",
            "size": [20.0, 140.0, 600.0],
            "pos": [255.0, 225.0, 0.0],
            "rot": [-0.0, 0.0, -3.14159],
            "quaternion": [0.0, 0.0, 1.0, 0.0],
            "dir": [1.6, 0.0, 0.0],
            "dims": [20.0, 140.0, 600.0],
        },
        {
            "id": "group_1_pe_frontal",
            "name": "Lateral Direita - Pé Frontal",
            "group": "group_1",
            "groupLabel": "Lateral Direita",
            "size": [20.0, 140.0, 450.0],
            "pos": [275.0, 225.0, 230.0],
            "rot": [1.5708, -0.0, -3.14159],
            "quaternion": [-0.0, -0.70711, 0.70711, 0.0],
            "dir": [1.6, 0.0, 0.0],
            "dims": [20.0, 140.0, 450.0],
        },
        {
            "id": "group_1_pe_traseiro",
            "name": "Lateral Direita - Pé Traseiro",
            "group": "group_1",
            "groupLabel": "Lateral Direita",
            "size": [20.0, 140.0, 450.0],
            "pos": [235.0, 225.0, -230.0],
            "rot": [1.5708, -0.0, -3.14159],
            "quaternion": [-0.0, -0.70711, 0.70711, 0.0],
            "dir": [1.6, 0.0, 0.0],
            "dims": [20.0, 140.0, 450.0],
        },
        {
            "id": "group_2_suporte_frente",
            "name": "Assento - Travessa Suporte Frontal",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [20.0, 70.0, 490.0],
            "pos": [-0.0, 258.0, 272.6],
            "rot": [1.7942, -1.5708, 0.0],
            "quaternion": [-0.55262, -0.44115, 0.55262, 0.44116],
            "dir": [0.0, 0.8, 1.2],
            "dims": [20.0, 70.0, 490.0],
        },
        {
            "id": "group_2_suporte_tras",
            "name": "Assento - Travessa Suporte Traseira",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [20.0, 70.0, 490.0],
            "pos": [-0.0, 173.8, -98.0],
            "rot": [1.7942, -1.5708, 0.0],
            "quaternion": [-0.55262, -0.44115, 0.55262, 0.44116],
            "dir": [0.0, 0.8, 1.2],
            "dims": [20.0, 70.0, 490.0],
        },
        {
            "id": "group_2_tabua_esq",
            "name": "Assento - Tábua Lateral Esquerda",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [20.0, 140.0, 450.0],
            "pos": [-175.0, 235.4, 82.8],
            "rot": [-0.2234, 0.0, 1.5708],
            "quaternion": [-0.07882, 0.07882, 0.7027, 0.7027],
            "dir": [0.0, 0.8, 1.2],
            "dims": [20.0, 140.0, 450.0],
        },
        {
            "id": "group_2_tabua_dir",
            "name": "Assento - Tábua Lateral Direita",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [20.0, 140.0, 450.0],
            "pos": [175.0, 235.4, 82.8],
            "rot": [-0.2234, 0.0, 1.5708],
            "quaternion": [-0.07882, 0.07882, 0.7027, 0.7027],
            "dir": [0.0, 0.8, 1.2],
            "dims": [20.0, 140.0, 450.0],
        },
        {
            "id": "group_2_tabua_centro",
            "name": "Assento - Tábua Central",
            "group": "group_2",
            "groupLabel": "Assento",
            "size": [20.0, 140.0, 450.0],
            "pos": [0.0, 235.4, 82.8],
            "rot": [-0.2234, 0.0, 1.5708],
            "quaternion": [-0.07882, 0.07882, 0.7027, 0.7027],
            "dir": [0.0, 0.8, 1.2],
            "dims": [20.0, 140.0, 450.0],
        },
        {
            "id": "group_3_tabua_esq",
            "name": "Encosto - Tábua Lateral Esquerda",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [20.0, 140.0, 445.0],
            "pos": [-155.0, 423.1, -261.7],
            "rot": [-2.00015, -0.0, -1.5708],
            "quaternion": [0.59504, 0.59504, 0.38201, -0.38201],
            "dir": [0.0, 1.2, -1.2],
            "dims": [20.0, 140.0, 445.0],
        },
        {
            "id": "group_3_tabua_centro",
            "name": "Encosto - Tábua Central",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [20.0, 140.0, 445.0],
            "pos": [-0.0, 423.1, -261.7],
            "rot": [-2.00015, -0.0, -1.5708],
            "quaternion": [0.59504, 0.59504, 0.38201, -0.38201],
            "dir": [0.0, 1.2, -1.2],
            "dims": [20.0, 140.0, 445.0],
        },
        {
            "id": "group_3_suporte_topo",
            "name": "Encosto - Travessa Traseira Superior",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [20.0, 70.0, 450.0],
            "pos": [0.0, 585.3, -357.9],
            "rot": [2.71224, 1.5708, 0.0],
            "quaternion": [0.69088, 0.15064, 0.69088, 0.15064],
            "dir": [0.0, 1.2, -1.2],
            "dims": [20.0, 70.0, 450.0],
        },
        {
            "id": "group_3_tabua_dir",
            "name": "Encosto - Tábua Lateral Direita",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [20.0, 140.0, 445.0],
            "pos": [155.0, 423.1, -261.7],
            "rot": [-2.00015, -0.0, -1.5708],
            "quaternion": [0.59504, 0.59504, 0.38201, -0.38201],
            "dir": [0.0, 1.2, -1.2],
            "dims": [20.0, 140.0, 445.0],
        },
        {
            "id": "group_3_suporte_base",
            "name": "Encosto - Travessa Traseira Inferior",
            "group": "group_3",
            "groupLabel": "Encosto",
            "size": [20.0, 70.0, 450.0],
            "pos": [0.0, 244.3, -201.8],
            "rot": [2.71224, 1.5708, 0.0],
            "quaternion": [0.69088, 0.15064, 0.69088, 0.15064],
            "dir": [0.0, 1.2, -1.2],
            "dims": [20.0, 70.0, 450.0],
        },
    ]
    return {
        "title": "Cadeira Krat (Gerrit Rietveld, 1934)",
        "dimensions": "590 x 630 x 686 mm",
        "description": "Design clássico modernista de 1934 em 4 módulos construtivos (18 peças de 20mm), sem peças soltas ou flutuando.",
        "pieces": pieces,
        "tools": recommend_tools("krat", doors=0, drawers=0),
        "assembly_guide": build_assembly_guide("krat", width=590, height=630, depth=686, thickness=20),
    }



def generate_krat_side_table_3d() -> Dict[str, Any]:
    """Gera o modelo 3D da Mesinha Lateral Krat (Gerrit Rietveld, 1934).
    
    Projetada com 13 peças de 20mm de espessura (larguras de 140mm e 70mm),
    aproveitando exatamente a sobra da chapa de Compensado Naval (2200x1600mm).
    """
    pieces: List[Dict[str, Any]] = [
        # Tampo Superior (3 Tábuas com espaçamento de 5mm para escoamento de água)
        {
            "id": "tampo_frontal",
            "name": "Tampo - Tábua Frontal",
            "group": "group_0",
            "groupLabel": "Tampo Superior",
            "size": [490.0, 20.0, 140.0],
            "pos": [0.0, 390.0, 145.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [0.0, 1.8, 0.4],
            "dims": [20.0, 140.0, 490.0],
        },
        {
            "id": "tampo_central",
            "name": "Tampo - Tábua Central",
            "group": "group_0",
            "groupLabel": "Tampo Superior",
            "size": [490.0, 20.0, 140.0],
            "pos": [0.0, 390.0, 0.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [0.0, 1.8, 0.0],
            "dims": [20.0, 140.0, 490.0],
        },
        {
            "id": "tampo_traseiro",
            "name": "Tampo - Tábua Traseira",
            "group": "group_0",
            "groupLabel": "Tampo Superior",
            "size": [490.0, 20.0, 140.0],
            "pos": [0.0, 390.0, -145.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [0.0, 1.8, -0.4],
            "dims": [20.0, 140.0, 490.0],
        },
        # Lateral Esquerda
        {
            "id": "pe_frontal_esq",
            "name": "Lateral Esq - Pé Frontal",
            "group": "group_1",
            "groupLabel": "Lateral Esquerda",
            "size": [20.0, 380.0, 140.0],
            "pos": [-210.0, 190.0, 140.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [-1.6, 0.0, 0.3],
            "dims": [20.0, 140.0, 380.0],
        },
        {
            "id": "pe_traseiro_esq",
            "name": "Lateral Esq - Pé Traseiro",
            "group": "group_1",
            "groupLabel": "Lateral Esquerda",
            "size": [20.0, 380.0, 140.0],
            "pos": [-210.0, 190.0, -140.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [-1.6, 0.0, -0.3],
            "dims": [20.0, 140.0, 380.0],
        },
        {
            "id": "travessa_topo_esq",
            "name": "Lateral Esq - Travessa Apoio Superior",
            "group": "group_1",
            "groupLabel": "Lateral Esquerda",
            "size": [20.0, 70.0, 420.0],
            "pos": [-190.0, 345.0, 0.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [-1.4, 0.4, 0.0],
            "dims": [20.0, 70.0, 420.0],
        },
        {
            "id": "travessa_base_esq",
            "name": "Lateral Esq - Travessa Base Inferior",
            "group": "group_1",
            "groupLabel": "Lateral Esquerda",
            "size": [20.0, 70.0, 420.0],
            "pos": [-190.0, 75.0, 0.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [-1.4, -0.3, 0.0],
            "dims": [20.0, 70.0, 420.0],
        },
        # Lateral Direita
        {
            "id": "pe_frontal_dir",
            "name": "Lateral Dir - Pé Frontal",
            "group": "group_2",
            "groupLabel": "Lateral Direita",
            "size": [20.0, 380.0, 140.0],
            "pos": [210.0, 190.0, 140.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [1.6, 0.0, 0.3],
            "dims": [20.0, 140.0, 380.0],
        },
        {
            "id": "pe_traseiro_dir",
            "name": "Lateral Dir - Pé Traseiro",
            "group": "group_2",
            "groupLabel": "Lateral Direita",
            "size": [20.0, 380.0, 140.0],
            "pos": [210.0, 190.0, -140.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [1.6, 0.0, -0.3],
            "dims": [20.0, 140.0, 380.0],
        },
        {
            "id": "travessa_topo_dir",
            "name": "Lateral Dir - Travessa Apoio Superior",
            "group": "group_2",
            "groupLabel": "Lateral Direita",
            "size": [20.0, 70.0, 420.0],
            "pos": [190.0, 345.0, 0.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [1.4, 0.4, 0.0],
            "dims": [20.0, 70.0, 420.0],
        },
        {
            "id": "travessa_base_dir",
            "name": "Lateral Dir - Travessa Base Inferior",
            "group": "group_2",
            "groupLabel": "Lateral Direita",
            "size": [20.0, 70.0, 420.0],
            "pos": [190.0, 75.0, 0.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [1.4, -0.3, 0.0],
            "dims": [20.0, 70.0, 420.0],
        },
        # Amarração Transversal
        {
            "id": "travessa_transversal_frente",
            "name": "Estrutura - Travessa Transversal Frontal",
            "group": "group_3",
            "groupLabel": "Amarração Transversal",
            "size": [360.0, 70.0, 20.0],
            "pos": [0.0, 345.0, 140.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [0.0, 0.0, 1.6],
            "dims": [20.0, 70.0, 360.0],
        },
        {
            "id": "travessa_transversal_tras",
            "name": "Estrutura - Travessa Transversal Traseira",
            "group": "group_3",
            "groupLabel": "Amarração Transversal",
            "size": [360.0, 70.0, 20.0],
            "pos": [0.0, 345.0, -140.0],
            "rot": [0.0, 0.0, 0.0],
            "dir": [0.0, 0.0, -1.6],
            "dims": [20.0, 70.0, 360.0],
        },
    ]

    return {
        "title": "Mesinha Lateral Krat (Gerrit Rietveld, 1934)",
        "dimensions": "490 x 440 x 400 mm",
        "description": "Mesa lateral modernista da família Crate Furniture (Kratmeubels, 1934) de Gerrit Rietveld. 13 peças de 20mm de espessura projetadas para aproveitar a sobra da chapa de compensado naval.",
        "pieces": pieces,
        "tools": recommend_tools("mesa", cuts_in_shop=False),
        "assembly_guide": build_assembly_guide("mesa", width=490, height=400, depth=440, thickness=20),
    }


def generate_cabinet_3d(
    width: float = 800.0,
    height: float = 600.0,
    depth: float = 350.0,
    thickness: float = 15.0,
    doors: int = 2,
    shelves: int = 1,
    drawers: int = 0,
) -> Dict[str, Any]:
    """Gera a estrutura 3D de um armário/gabinete completo com portas, prateleiras e gavetas."""
    internal_w = width - (2 * thickness)
    internal_d = depth - thickness  # desconta fundo se houver
    half_w = width / 2.0
    half_h = height / 2.0
    half_d = depth / 2.0

    pieces: List[Dict[str, Any]] = [
        {
            "id": "lat_esq",
            "name": "Lateral Esquerda",
            "size": [thickness, height, depth],
            "pos": [-half_w + (thickness / 2.0), half_h, 0],
            "rot": [0, 0, 0],
            "dir": [-1.2, 0, 0],
        },
        {
            "id": "lat_dir",
            "name": "Lateral Direita",
            "size": [thickness, height, depth],
            "pos": [half_w - (thickness / 2.0), half_h, 0],
            "rot": [0, 0, 0],
            "dir": [1.2, 0, 0],
        },
        {
            "id": "tampo_sup",
            "name": "Tampo Superior",
            "size": [internal_w, thickness, depth],
            "pos": [0, height - (thickness / 2.0), 0],
            "rot": [0, 0, 0],
            "dir": [0, 1.2, 0],
        },
        {
            "id": "base_inf",
            "name": "Base Inferior",
            "size": [internal_w, thickness, depth],
            "pos": [0, thickness / 2.0, 0],
            "rot": [0, 0, 0],
            "dir": [0, -1.2, 0],
        },
        # Fundo em MDF 6mm
        {
            "id": "fundo",
            "name": "Fundo (MDF 6mm)",
            "size": [internal_w + 10.0, height - 10.0, 6.0],
            "pos": [0, half_h, -half_d + 3.0],
            "rot": [0, 0, 0],
            "dir": [0, 0, -1.5],
        },
    ]

    # Prateleiras internas
    if shelves > 0:
        spacing = (height - 2 * thickness) / (shelves + 1)
        for i in range(shelves):
            y_pos = thickness + (i + 1) * spacing
            pieces.append({
                "id": f"prateleira_{i+1}",
                "name": f"Prateleira Interna {i+1}",
                "size": [internal_w - 2.0, thickness, internal_d - 20.0],
                "pos": [0, y_pos, 0],
                "rot": [0, 0, 0],
                "dir": [0, 0, 0.8],
            })

    # Portas
    if doors == 2:
        door_w = (width - 4.0 - 3.0) / 2.0
        door_h = height - 4.0
        pieces.append({
            "id": "porta_esq",
            "name": "Porta Esquerda",
            "size": [round(door_w, 1), round(door_h, 1), thickness],
            "pos": [-door_w / 2.0 - 1.5, half_h, half_d + (thickness / 2.0)],
            "rot": [0, 0, 0],
            "dir": [-0.6, 0, 1.5],
        })
        pieces.append({
            "id": "porta_dir",
            "name": "Porta Direita",
            "size": [round(door_w, 1), round(door_h, 1), thickness],
            "pos": [door_w / 2.0 + 1.5, half_h, half_d + (thickness / 2.0)],
            "rot": [0, 0, 0],
            "dir": [0.6, 0, 1.5],
        })
    elif doors == 1:
        door_w = width - 4.0
        door_h = height - 4.0
        pieces.append({
            "id": "porta_unica",
            "name": "Porta Única",
            "size": [round(door_w, 1), round(door_h, 1), thickness],
            "pos": [0, half_h, half_d + (thickness / 2.0)],
            "rot": [0, 0, 0],
            "dir": [0, 0, 1.5],
        })

    return {
        "title": f"Armário ({width:.0f}x{height:.0f}x{depth:.0f}mm)",
        "dimensions": f"{width:.0f} x {height:.0f} x {depth:.0f} mm",
        "description": f"Armário em MDF {thickness:.0f}mm com {doors} porta(s) e {shelves} prateleira(s).",
        "pieces": pieces,
        "tools": recommend_tools("armario", doors=doors, drawers=drawers),
        "assembly_guide": build_assembly_guide("armario", width=width, height=height, depth=depth, thickness=thickness, doors=doors, shelves=shelves, drawers=drawers),
    }


def generate_niche_3d(
    width: float = 600.0,
    height: float = 400.0,
    depth: float = 200.0,
    thickness: float = 15.0,
    with_back: bool = True,
) -> Dict[str, Any]:
    """Gera o modelo 3D de um nicho retangular de parede."""
    internal_w = width - (2 * thickness)
    internal_h = height - (2 * thickness)
    half_w = width / 2.0
    half_h = height / 2.0
    half_d = depth / 2.0

    pieces: List[Dict[str, Any]] = [
        {
            "id": "tampo_sup",
            "name": "Tampo Superior",
            "size": [width, thickness, depth],
            "pos": [0, height - (thickness / 2.0), 0],
            "rot": [0, 0, 0],
            "dir": [0, 1.2, 0],
        },
        {
            "id": "base_inf",
            "name": "Base Inferior",
            "size": [width, thickness, depth],
            "pos": [0, thickness / 2.0, 0],
            "rot": [0, 0, 0],
            "dir": [0, -1.2, 0],
        },
        {
            "id": "lat_esq",
            "name": "Lateral Esquerda",
            "size": [thickness, internal_h, depth],
            "pos": [-half_w + (thickness / 2.0), half_h, 0],
            "rot": [0, 0, 0],
            "dir": [-1.2, 0, 0],
        },
        {
            "id": "lat_dir",
            "name": "Lateral Direita",
            "size": [thickness, internal_h, depth],
            "pos": [half_w - (thickness / 2.0), half_h, 0],
            "rot": [0, 0, 0],
            "dir": [1.2, 0, 0],
        },
    ]

    if with_back:
        pieces.append({
            "id": "fundo",
            "name": "Fundo (MDF 6mm)",
            "size": [width - 20.0, height - 20.0, 6.0],
            "pos": [0, half_h, -half_d + 3.0],
            "rot": [0, 0, 0],
            "dir": [0, 0, -1.5],
        })

    return {
        "title": f"Nicho de Parede ({width:.0f}x{height:.0f}x{depth:.0f}mm)",
        "dimensions": f"{width:.0f} x {height:.0f} x {depth:.0f} mm",
        "description": f"Nicho em MDF {thickness:.0f}mm.",
        "pieces": pieces,
        "tools": recommend_tools("nicho", doors=0, drawers=0),
        "assembly_guide": build_assembly_guide("nicho", width=width, height=height, depth=depth, thickness=thickness),
    }


def generate_bookshelf_3d(
    width: float = 800.0,
    height: float = 1800.0,
    depth: float = 300.0,
    thickness: float = 18.0,
    shelves_count: int = 4,
) -> Dict[str, Any]:
    """Gera uma estante de livros de piso."""
    internal_w = width - (2 * thickness)
    half_w = width / 2.0
    half_h = height / 2.0
    half_d = depth / 2.0

    pieces: List[Dict[str, Any]] = [
        {
            "id": "lat_esq",
            "name": "Lateral Esquerda",
            "size": [thickness, height, depth],
            "pos": [-half_w + (thickness / 2.0), half_h, 0],
            "rot": [0, 0, 0],
            "dir": [-1.2, 0, 0],
        },
        {
            "id": "lat_dir",
            "name": "Lateral Direita",
            "size": [thickness, height, depth],
            "pos": [half_w - (thickness / 2.0), half_h, 0],
            "rot": [0, 0, 0],
            "dir": [1.2, 0, 0],
        },
        {
            "id": "tampo_sup",
            "name": "Tampo Superior",
            "size": [internal_w, thickness, depth],
            "pos": [0, height - (thickness / 2.0), 0],
            "rot": [0, 0, 0],
            "dir": [0, 1.2, 0],
        },
        {
            "id": "base_inf",
            "name": "Base Inferior (com rodapé)",
            "size": [internal_w, thickness, depth],
            "pos": [0, 70.0 + (thickness / 2.0), 0],
            "rot": [0, 0, 0],
            "dir": [0, -0.8, 0],
        },
        {
            "id": "rodape_frontal",
            "name": "Rodapé Frontal",
            "size": [internal_w, 70.0, thickness],
            "pos": [0, 35.0, half_d - (thickness / 2.0)],
            "rot": [0, 0, 0],
            "dir": [0, -0.4, 1.0],
        },
    ]

    # Prateleiras intermediárias
    usable_h = (height - (70.0 + thickness) - thickness)
    spacing = usable_h / (shelves_count + 1)
    for i in range(shelves_count):
        y_pos = (70.0 + thickness) + (i + 1) * spacing
        pieces.append({
            "id": f"prateleira_{i+1}",
            "name": f"Prateleira {i+1}",
            "size": [internal_w, thickness, depth - 5.0],
            "pos": [0, y_pos, 0],
            "rot": [0, 0, 0],
            "dir": [0, 0, 0.7],
        })

    return {
        "title": f"Estante de Livros ({width:.0f}x{height:.0f}x{depth:.0f}mm)",
        "dimensions": f"{width:.0f} x {height:.0f} x {depth:.0f} mm",
        "description": f"Estante robusta em MDF {thickness:.0f}mm com {shelves_count} prateleiras.",
        "pieces": pieces,
        "tools": recommend_tools("estante", doors=0, drawers=0),
        "assembly_guide": build_assembly_guide("estante", width=width, height=height, depth=depth, thickness=thickness, shelves=shelves_count),
    }


def slugify_name(text: str) -> str:
    """Converte o título do projeto em um nome de arquivo seguro (slug sem acentos)."""
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s-]+', '_', text).strip('_')
    return text or "projeto"


def save_current_project(project_data: Dict[str, Any], custom_filename: Optional[str] = None) -> Dict[str, str]:
    """Salva o projeto tanto como projeto ativo (viewer/current_project.js/json)
    quanto como arquivo individual permanente na pasta viewer/projects/.

    A inclusão via arquivo .js contendo window.CURRENT_PROJECT permite que o arquivo index.html
    carregue os dados sem bloqueio de CORS mesmo quando aberto diretamente pelo protocolo file://.
    """
    base_repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    viewer_dir = os.path.join(base_repo, "viewer")
    os.makedirs(viewer_dir, exist_ok=True)

    # 1. Salva como projeto ativo atual
    json_path = os.path.join(viewer_dir, "current_project.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)

    js_path = os.path.join(viewer_dir, "current_project.js")
    with open(js_path, "w", encoding="utf-8") as f:
        js_content = f"// Gerado automaticamente pelo assistente de marcenaria\nwindow.CURRENT_PROJECT = {json.dumps(project_data, indent=2, ensure_ascii=False)};\n"
        f.write(js_content)

    # 2. Salva também permanentemente na pasta viewer/projects/
    projects_dir = os.path.join(viewer_dir, "projects")
    os.makedirs(projects_dir, exist_ok=True)

    slug = custom_filename if custom_filename else f"{slugify_name(project_data.get('title', 'projeto'))}.json"
    if not slug.endswith('.json'):
        slug += '.json'

    archive_path = os.path.join(projects_dir, slug)
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)

    return {
        "json_path": json_path,
        "js_path": js_path,
        "archive_path": archive_path,
    }

def export_project_to_file(project_data: Dict[str, Any], filename: str = "project.json") -> str:
    """Exporta os dados do projeto para a pasta viewer/projects/."""
    base_repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_repo, "viewer", "projects")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, filename)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)
    return out_file



def build_assembly_guide(
    furniture_type: str,
    width: float = 800.0,
    height: float = 600.0,
    depth: float = 350.0,
    thickness: float = 15.0,
    doors: int = 0,
    shelves: int = 0,
    drawers: int = 0
) -> Dict[str, Any]:
    """Constrói o roteiro sequencial estruturado de montagem profissional para o móvel."""
    f_type = furniture_type.lower()
    
    if "krat" in f_type or "cadeira" in f_type:
        return {
            "estimated_time_hours": 3.0,
            "difficulty": "Médio (Requer conferência de esquadro e pré-furações)",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Conferência e Pré-Furação dos 4 Módulos",
                    "description": "Separe as 18 peças de Pinus 20mm nos seus respectivos grupos (2x Laterais, Assento e Encosto).",
                    "steps": [
                        "Identifique os 4 grupos: Grupo 0 (Lateral Esquerda), Grupo 1 (Lateral Direita), Grupo 2 (Assento) e Grupo 3 (Encosto).",
                        "Marque todas as furações com esquadro e lápis. As tábuas de Pinus racham se parafusadas sem furo piloto.",
                        "Execute furações piloto com broca 3.0mm e escareador 45° na profundidade exata da cabeça do parafuso.",
                        "Lixe suavemente as arestas com lixa grão 180 para quebrar cantos vivos e eliminar farpas."
                    ],
                    "tips": "Utilize um sargento para segurar peças sobrepostas antes de furar, garantindo alinhamento perfeito."
                },
                {
                    "phase_number": 2,
                    "title": "Montagem das Laterais Esquerda e Direita (Módulos 0 e 1)",
                    "description": "Monte os dois quadros laterais tipo caixote com montantes dianteiro/traseiro, travessa larga e apoio de braço.",
                    "steps": [
                        "Una o Pé Frontal (20x140x450mm) e o Pé Traseiro (20x140x450mm) à Travessa Larga (20x140x600mm) formando o sanduíche lateral.",
                        "Fixe com 2 a 3 parafusos 4.0x40mm em cada encontro, conferindo 90° com esquadro metálico.",
                        "Posicione o Apoio de Braço plano (20x70x600mm) deitado sobre o topo dos pés (Y=450 a 470mm) e parafuse de cima para baixo escareando bem.",
                        "Repita a montagem para a Lateral Direita de forma perfeitamente espelhada."
                    ],
                    "tips": "Coloque as duas laterais lado a lado no chão plano para garantir que os pés tocam o solo no mesmo nível."
                },
                {
                    "phase_number": 3,
                    "title": "Montagem do Módulo do Assento (Módulo 2)",
                    "description": "Construção do estrado do assento composto por 2 travessas inferiores de 490mm e 3 tábuas superiores.",
                    "steps": [
                        "Posicione as 2 Travessas de Suporte (20x70x490mm) paralelas a 380mm de distância uma da outra.",
                        "Acomode as 3 Tábuas do Assento (20x140x450mm) apoiadas perpendicularmente sobre as travessas.",
                        "Ajuste os vãos laterais uniformes de 35mm entre as tábuas (use um espaçador de madeira de 35mm como gabarito).",
                        "Parafuse as tábuas nas travessas de suporte com parafusos 4.0x40mm de baixo para cima ou por cima escareado."
                    ],
                    "tips": "O módulo do assento formará uma grelha rígida de 490mm de largura que se encaixará justo entre as laterais."
                },
                {
                    "phase_number": 4,
                    "title": "Montagem do Módulo do Encosto (Módulo 3)",
                    "description": "Construção do painel traseiro inclinado com 3 tábuas verticais travadas por 2 travessas traseiras.",
                    "steps": [
                        "Alinhe as 3 Tábuas Verticais (20x140x445mm) no piso com espaçamento uniforme de 15mm entre si.",
                        "Posicione a Travessa Traseira Superior (20x70x450mm) no topo e a Travessa Traseira Inferior (20x70x450mm) na base.",
                        "Parafuse as travessas por trás das tábuas verticais para manter a face frontal limpa e lisa para o encosto das costas."
                    ],
                    "tips": "Certifique-se de que a largura total deste módulo seja 450mm, correspondente ao vão livre interno das laterais."
                },
                {
                    "phase_number": 5,
                    "title": "União Estrutural e Acabamento",
                    "description": "Junção dos 4 módulos principais no ângulo correto de inclinação Rietveld.",
                    "steps": [
                        "Posicione as duas laterais verticais apoiadas no chão com espaçamento de 490mm.",
                        "Encaixe o módulo do assento com inclinação ergonômica de ~12.8° e parafuse as travessas de 490mm nas faces internas das laterais.",
                        "Encaixe o módulo do encosto com inclinação de ~24.6° apoiando a base sobre as travessas do assento e parafuse firmemente.",
                        "Aplique tapa-furos ou massa para madeira nos parafusos aparentes e finalize com óleo mineral, seladora ou verniz fosco."
                    ],
                    "tips": "Teste a estabilidade da cadeira sobre uma superfície plana e aplique feltros adesivos na base dos pés para proteger o piso."
                }
            ]
        }
    
    elif "mesa" in f_type:
        return {
            "estimated_time_hours": 1.5,
            "difficulty": "Fácil / Médio (Montagem por esquadro em 90°)",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Conferência e Pré-Furação das Peças",
                    "description": "Separe as 13 peças de compensado naval 20mm (3 do tampo, 4 pés e 6 travessas).",
                    "steps": [
                        "Identifique as peças: 3 tábuas do tampo (490x140mm), 4 pés verticais (380x140mm), 4 travessas laterais (420x70mm) e 2 transversais (360x70mm).",
                        "Lixe suavemente as arestas com lixa grão 150 para quebrar cantos vivos.",
                        "Execute furações piloto com broca 3.0mm e escareador nos pontos de união dos parafusos."
                    ],
                    "tips": "Escareie cerca de 2mm para que a cabeça dos parafusos fique ligeiramente embutida."
                },
                {
                    "phase_number": 2,
                    "title": "Montagem dos Quadros Laterais (Pernas)",
                    "description": "Monte os dois quadros laterais rígidos em formato retangular.",
                    "steps": [
                        "Una o Pé Frontal e o Pé Traseiro à Travessa de Apoio Superior (420x70mm) rente ao topo a 380mm do chão.",
                        "Fixe a Travessa Base Inferior (420x70mm) a 40mm do chão, mantendo 90° com esquadro metálico.",
                        "Repita a operação para a Lateral Direita de forma perfeitamente idêntica."
                    ],
                    "tips": "Apoie os dois quadros no chão nivelado para conferir se as alturas estão rigorosamente iguais."
                },
                {
                    "phase_number": 3,
                    "title": "Travamento Transversal da Base",
                    "description": "Una as duas laterais com as travessas transversais para criar uma estrutura tridimensional indeformável.",
                    "steps": [
                        "Posicione a Travessa Transversal Frontal (360x70mm) e a Traseira (360x70mm) entre os quadros laterais.",
                        "Parafuse firmemente por dentro nas travessas de apoio superior.",
                        "Meça as diagonais com a trena para garantir esquadro perfeito."
                    ],
                    "tips": "Diagonais com a mesma medida garantem que a mesinha não balance nem torça."
                },
                {
                    "phase_number": 4,
                    "title": "Fixação das Tábuas do Tampo Ripada",
                    "description": "Fixação das 3 tábuas de 490x140mm no topo da estrutura.",
                    "steps": [
                        "Posicione as 3 tábuas com saliência simétrica de 25mm nas extremidades.",
                        "Mantenha um vão uniforme de 5mm entre as tábuas para drenagem de água da chuva.",
                        "Parafuse de cima para baixo nas travessas de apoio superior (ou por baixo com cantoneiras se preferir fixação oculta)."
                    ],
                    "tips": "O vão de 5mm previne acúmulo de água no tampo e combina perfeitamente com o estrado da Cadeira Krat."
                },
                {
                    "phase_number": 5,
                    "title": "Proteção e Acabamento para Uso Externo",
                    "description": "Impermeabilização com Stain e instalação de sapatas protetoras.",
                    "steps": [
                        "Limpe o pó e aplique 2 a 3 demãos de Stain Polisten Incolor ou tonalizado (Sayerlack).",
                        "Instale sapatas plásticas de 5mm embaixo dos 4 pés para proteger do contato com piso molhado."
                    ],
                    "tips": "O Stain penetra na madeira sem criar película quebradiça, garantindo anos de durabilidade no jardim."
                }
            ]
        }

    elif "nicho" in f_type:
        return {
            "estimated_time_hours": 1.5,
            "difficulty": "Fácil (Excelente projeto para iniciantes)",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Conferência e Fita de Borda",
                    "description": "Preparação das 4 peças da caixaria e do fundo.",
                    "steps": [
                        "Identifique: 2 Laterais, 1 Base, 1 Tampo e 1 Fundo (MDF 6mm).",
                        "Aplique fita de borda nas arestas frontais visíveis com cola de contato ou fita termocolante.",
                        "Refile o excesso de fita com estilete ou refilador duplo e quebre a quina com lixa 220."
                    ],
                    "tips": "Cuidado para não aprofundar o estilete no MDF durante o refile."
                },
                {
                    "phase_number": 2,
                    "title": "Pré-Furação e Montagem da Caixaria",
                    "description": "União das peças estruturais com esquadro de 90°.",
                    "steps": [
                        "Marque 2 furos por junção nas faces das peças externas (recuo de 35mm da frente e do fundo).",
                        "Execute furo piloto de 3mm com escareador na espessura de 15mm.",
                        "Prenda a Lateral à Base com grampo angular 90° e aperte os parafusos 4.0x40mm com torque moderado.",
                        "Repita a operação para a outra lateral e finalize com o tampo superior."
                    ],
                    "tips": "Nunca aperte parafusos de topo em MDF sem pré-furação para não abrir a chapa."
                },
                {
                    "phase_number": 3,
                    "title": "Esquadro e Travamento com o Fundo",
                    "description": "Garantia de estabilidade e geometria perfeita do nicho.",
                    "steps": [
                        "Meça as duas diagonais do nicho com a trena. Elas devem ter rigorosamente o mesmo comprimento milimétrico.",
                        "Posicione o fundo de 6mm no rebaixo traseiro e parafuse a cada 15cm com parafusos 3.0x20mm.",
                        "O fundo parafusado travará o esquadro definitivamente, impedindo o nicho de deformar."
                    ],
                    "tips": "Se uma diagonal estiver maior, empurre suavemente o canto oposto antes de parafusar o fundo."
                },
                {
                    "phase_number": 4,
                    "title": "Fixação na Parede",
                    "description": "Instalação suspensa segura.",
                    "steps": [
                        "Fixe 2 suportes cantoneira com capa plástica nos cantos superiores internos do nicho.",
                        "Nivele o nicho na parede com nível de bolha e marque os furos com lápis.",
                        "Fure a alvenaria com broca de vídea 8mm, insira as buchas e fixe o móvel com parafusos 5.0x50mm."
                    ],
                    "tips": "Utilize as capas plásticas na cor do MDF para esconder completamente as ferragens de sustentação."
                }
            ]
        }

    elif "estante" in f_type or "livro" in f_type:
        return {
            "estimated_time_hours": 3.5,
            "difficulty": "Médio (Atenção ao alinhamento de prateleiras)",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Gabarito e Marcação das Prateleiras",
                    "description": "Alinhamento das alturas para garantir prateleiras 100% niveladas.",
                    "steps": [
                        "Coloque as duas laterais lado a lado no chão com a face interna voltada para cima.",
                        "Utilize esquadro metálico e trena para traçar a linha de centro de cada prateleira em ambas as laterais simultaneamente.",
                        "Marque 2 pontos de furação em cada linha de prateleira (recuos de 50mm de cada borda).",
                        "Faça furações passantes de 3mm escareadas pela face externa das laterais."
                    ],
                    "tips": "Marcar as duas laterais juntas garante que as prateleiras não fiquem tortas."
                },
                {
                    "phase_number": 2,
                    "title": "Montagem da Base, Rodapé e Prateleiras",
                    "description": "Fixação progressiva de baixo para cima.",
                    "steps": [
                        "Fixe o rodapé frontal recuado 15mm da frente da base inferior.",
                        "Fixe a base inferior nas laterais com parafusos 4.0x40mm.",
                        "Fixe as prateleiras intermediárias uma a uma, apoiando-as com auxílio de grampos sargentos.",
                        "Finalize com a instalação do tampo superior."
                    ],
                    "tips": "Apoie a estante deitada de lado sobre uma bancada ou tapete para não riscar a pintura."
                },
                {
                    "phase_number": 3,
                    "title": "Fixação do Fundo e Travamento Anti-Tombamento",
                    "description": "Segurança e rigidez estrutural.",
                    "steps": [
                        "Confira a igualdade das diagonais da estante.",
                        "Pregue ou parafuse o fundo de 6mm em todo o perímetro e também nas prateleiras centrais.",
                        "Instale um suporte de travamento de segurança tipo L no topo da estante ancorado na parede contra tombamento acidental."
                    ],
                    "tips": "Móveis com altura superior a 1,20m devem sempre ter fixação anti-tombamento na parede."
                }
            ]
        }

    else: # Armário padrão
        return {
            "estimated_time_hours": 4.0,
            "difficulty": "Médio-Avançado (Envolve dobradiças e portas)",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Fita de Borda e Preparação dos Calços",
                    "description": "Aplicação de fita nas arestas visíveis e furações das ferragens.",
                    "steps": [
                        "Aplique fita de borda nas frentes de todas as peças e em todos os 4 lados das portas.",
                        "Se as portas não vierem furadas de fábrica, use a broca caneco de 35mm para fazer as cavidades de 11.5mm com centro a 22mm da borda.",
                        "Parafuse os calços das dobradiças nas marcas das laterais com parafusos 3.5x16mm."
                    ],
                    "tips": "Não ultrapasse 11.5mm de profundidade no furo do caneco para não atravessar a face da porta."
                },
                {
                    "phase_number": 2,
                    "title": "Montagem da Caixaria Principal",
                    "description": "União estrutural de base, laterais e tampo.",
                    "steps": [
                        "Una a Lateral Esquerda à Base com grampos 90° e parafuse com parafusos 4.0x40mm escareados.",
                        "Instale a Lateral Direita e em seguida o Tampo Superior.",
                        "Instale a prateleira intermediária caso o armário possua divisória interna."
                    ],
                    "tips": "Use torque baixo na parafusadeira para dar o aperto final manualmente com chave de fenda."
                },
                {
                    "phase_number": 3,
                    "title": "Esquadro e Fundo Traseiro",
                    "description": "Travamento da estrutura antes da instalação das portas.",
                    "steps": [
                        "Meça as diagonais com a trena e ajuste até ficarem rigorosamente iguais.",
                        "Fixe o fundo de 6mm com parafusos 3.0x20mm a cada 15cm por todo o contorno.",
                        "Instale as cantoneiras reforçadas de fixação na parede nos cantos superiores internos."
                    ],
                    "tips": "Um armário fora de esquadro impedirá que as portas fiquem alinhadas."
                },
                {
                    "phase_number": 4,
                    "title": "Instalação e Regulagem das Portas",
                    "description": "Encaixe das dobradiças e alinhamento milimétrico das frestas.",
                    "steps": [
                        "Fixe as dobradiças caneco nas portas com parafusos 3.5x16mm.",
                        "Encaixe o braço da dobradiça no calço da lateral (sistema click ou parafuso de fixação).",
                        "Regule os 3 parafusos da dobradiça: profundidade (afastamento da caixa), altura (nível) e lateral (fresta central entre as portas).",
                        "Cole os batentes de silicone anti-impacto no canto oposto às dobradiças."
                    ],
                    "tips": "A fresta central recomendada entre duas portas de giro é de 3mm a 4mm."
                }
            ]
        }
