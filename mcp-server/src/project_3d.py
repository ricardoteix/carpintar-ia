"""Gerador de dados 3D, cálculos paramétricos de móveis e exportador para o visualizador."""

from typing import Any, Dict, List, Optional
import json
import math
import os


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
    }


def save_current_project(project_data: Dict[str, Any]) -> Dict[str, str]:
    """Salva o projeto tanto como viewer/current_project.js quanto viewer/current_project.json.

    A inclusão via arquivo .js contendo window.CURRENT_PROJECT permite que o arquivo index.html
    carregue os dados sem bloqueio de CORS mesmo quando aberto diretamente pelo protocolo file://.
    """
    base_repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    viewer_dir = os.path.join(base_repo, "viewer")
    os.makedirs(viewer_dir, exist_ok=True)

    json_path = os.path.join(viewer_dir, "current_project.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)

    js_path = os.path.join(viewer_dir, "current_project.js")
    with open(js_path, "w", encoding="utf-8") as f:
        js_content = f"// Gerado automaticamente pelo assistente de marcenaria\nwindow.CURRENT_PROJECT = {json.dumps(project_data, indent=2, ensure_ascii=False)};\n"
        f.write(js_content)

    return {
        "json_path": json_path,
        "js_path": js_path,
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

