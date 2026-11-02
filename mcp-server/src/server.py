"""Servidor FastMCP para apoio à Marcenaria com integração aos dados da Leo Madeiras."""

from typing import Any, Dict, List, Optional
try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP

from src.leo_client import LeoMadeirasClient
from src.rules import recommend_hardware
from src.cutlist_optimizer import optimize_cutting_plan
from src.project_3d import (
    generate_cabinet_3d,
    generate_krat_chair_3d,
    generate_krat_side_table_3d,
    generate_niche_3d,
    generate_bookshelf_3d,
    export_project_to_file,
    save_current_project,
)

# Inicializa o servidor FastMCP
mcp = FastMCP(
    "carpintaria-leo-madeiras",
    description="Servidor MCP para busca de materiais de marcenaria na Leo Madeiras e cálculo de ferragens",
)

client = LeoMadeirasClient()


@mcp.tool()
async def search_materials(
    query: str,
    thickness: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    sort: str = "relevance",
) -> Dict[str, Any]:
    """Busca materiais, chapas de MDF, ferragens, fitas e químicos na Leo Madeiras.

    Args:
        query: Termo de busca (ex: 'MDF Branco', 'Dobradiça caneco 35mm', 'Corrediça 450mm')
        thickness: Filtro de espessura opcional (ex: '15mm', '18mm', '6mm')
        limit: Quantidade de produtos a retornar (máx 50, padrão 10)
        offset: Índice inicial para paginação
        sort: Ordenação dos produtos (padrão 'relevance')
    """
    return await client.search_products(
        query=query,
        thickness=thickness,
        limit=limit,
        offset=offset,
        sort=sort,
    )


@mcp.tool()
async def suggest_terms(query: str) -> Dict[str, Any]:
    """Retorna sugestões de termos de busca e produtos rápidos do catálogo da Leo Madeiras.

    Args:
        query: Termo parcial para autocomplete (ex: 'Pinus', 'MDF', 'Fita')
    """
    return await client.get_suggestions(query=query)


@mcp.tool()
def recommend_hardware_kit(
    furniture_type: str,
    pieces_count: int = 4,
    doors: int = 0,
    door_height_mm: float = 600.0,
    drawers: int = 0,
    linear_edge_meters: Optional[float] = None,
    sheet_thickness_mm: int = 15,
) -> Dict[str, Any]:
    """Calcula a lista recomendada de insumos de montagem (parafusos, dobradiças, corrediças, fita e fixadores).

    Args:
        furniture_type: Tipo do móvel ('nicho', 'armario', 'gaveteiro', 'prateleira', etc.)
        pieces_count: Quantidade total estimada de peças de corte da caixaria
        doors: Quantidade de portas
        door_height_mm: Altura média das portas em mm (padrão 600mm)
        drawers: Quantidade de gavetas
        linear_edge_meters: Metragem estimada de fita de borda (opcional)
        sheet_thickness_mm: Espessura da chapa em mm (15 ou 18)
    """
    return recommend_hardware(
        furniture_type=furniture_type,
        pieces_count=pieces_count,
        doors=doors,
        door_height_mm=door_height_mm,
        drawers=drawers,
        linear_edge_meters=linear_edge_meters,
        sheet_thickness_mm=sheet_thickness_mm,
    )


@mcp.tool()
def calculate_cutting_plan(
    pieces: List[Dict[str, Any]],
    sheet_width: float = 2750.0,
    sheet_height: float = 1830.0,
    kerf: float = 4.0,
    margin: float = 10.0,
    allow_rotation: bool = True,
) -> Dict[str, Any]:
    """Calcula o plano de corte 2D (bin-packing de guilhotina) para lista de peças em chapas retangulares.

    Args:
        pieces: Lista de peças, ex: [{'name': 'Lateral', 'length': 600, 'width': 350, 'quantity': 2, 'can_rotate': True}]
        sheet_width: Comprimento da chapa inteira em mm (padrão 2750mm para MDF)
        sheet_height: Largura da chapa inteira em mm (padrão 1830mm para MDF)
        kerf: Espessura da lâmina de corte em mm (padrão 4mm)
        margin: Margem de refile de esquadro nas bordas da chapa em mm (padrão 10mm)
        allow_rotation: Se True, permite rotacionar as peças em 90 graus para melhor encaixe
    """
    return optimize_cutting_plan(
        pieces=pieces,
        sheet_width=sheet_width,
        sheet_height=sheet_height,
        kerf=kerf,
        margin=margin,
        allow_rotation=allow_rotation,
    )


@mcp.tool()
def export_3d_project(
    furniture_type: str = "armario",
    width: float = 800.0,
    height: float = 600.0,
    depth: float = 350.0,
    thickness: float = 15.0,
    doors: int = 2,
    filename: str = "custom_project.json",
) -> Dict[str, Any]:
    """Exporta as coordenadas e vetores de visão explodida de um projeto para o visualizador 3D.

    Args:
        furniture_type: Tipo do móvel ('armario', 'nicho', etc.)
        width: Largura externa em mm
        height: Altura externa em mm
        depth: Profundidade externa em mm
        thickness: Espessura da chapa em mm
        doors: Quantidade de portas (1 ou 2)
        filename: Nome do arquivo JSON a salvar em viewer/projects/
    """
    project_data = generate_cabinet_3d(
        width=width,
        height=height,
        depth=depth,
        thickness=thickness,
        doors=doors,
    )
    saved_path = export_project_to_file(project_data=project_data, filename=filename)
    return {
        "status": "success",
        "project_title": project_data["title"],
        "total_pieces": len(project_data["pieces"]),
        "file_path": saved_path,
        "instructions": (
            f"Arquivo salvo com sucesso em '{saved_path}'. "
            "Abra 'viewer/index.html' no navegador e clique em 'Carregar JSON' para inspecionar em 3D com visão explodida."
        ),
    }


@mcp.tool()
def preview_furniture_3d(
    furniture_type: str = "krat",
    width: float = 800.0,
    height: float = 600.0,
    depth: float = 350.0,
    thickness: float = 15.0,
    doors: int = 2,
    shelves: int = 1,
) -> Dict[str, Any]:
    """Gera a cena 3D com visão explodida do móvel discutido no chat e atualiza o visualizador local.

    Args:
        furniture_type: 'krat' (Cadeira Rietveld), 'armario', 'nicho', 'estante'
        width: Largura externa em mm
        height: Altura externa em mm
        depth: Profundidade externa em mm
        thickness: Espessura da chapa em mm
        doors: Quantidade de portas (para armário)
        shelves: Quantidade de prateleiras (para armário ou estante)
    """
    f_type = furniture_type.lower()
    if "mesa" in f_type:
        project_data = generate_krat_side_table_3d()
    elif "krat" in f_type or "cadeira" in f_type:
        project_data = generate_krat_chair_3d()
    elif "nicho" in f_type:
        project_data = generate_niche_3d(
            width=width, height=height, depth=depth, thickness=thickness
        )
    elif "estante" in f_type or "livro" in f_type:
        project_data = generate_bookshelf_3d(
            width=width, height=height, depth=depth, thickness=thickness, shelves_count=shelves
        )
    else:
        project_data = generate_cabinet_3d(
            width=width, height=height, depth=depth, thickness=thickness, doors=doors, shelves=shelves
        )

    saved_info = save_current_project(project_data)
    return {
        "status": "success",
        "project_title": project_data["title"],
        "total_pieces": len(project_data["pieces"]),
        "dimensions": project_data["dimensions"],
        "viewer_file": "viewer/index.html",
        "message": (
            f"O projeto '{project_data['title']}' foi renderizado e salvo como o projeto ativo do chat! "
            "Abra ou recarregue 'viewer/index.html' no seu navegador para inspecionar em 3D com visão explodida."
        ),
    }




@mcp.tool()
def generate_assembly_manual(
    furniture_type: str = "krat",
    width: float = 800.0,
    height: float = 600.0,
    depth: float = 350.0,
    thickness: float = 15.0,
    doors: int = 2,
    shelves: int = 1,
) -> Dict[str, Any]:
    """Gera o manual de montagem passo a passo, lista de ferramentas e EPIs para o móvel.

    Atualiza o projeto ativo no visualizador local (viewer/) e retorna o manual em texto formatado.

    Args:
        furniture_type: 'krat' (Cadeira Rietveld), 'armario', 'nicho', 'estante'
        width: Largura externa em mm
        height: Altura externa em mm
        depth: Profundidade externa em mm
        thickness: Espessura da chapa em mm
        doors: Quantidade de portas (para armário)
        shelves: Quantidade de prateleiras (para armário ou estante)
    """
    f_type = furniture_type.lower()
    if "mesa" in f_type:
        project_data = generate_krat_side_table_3d()
    elif "krat" in f_type or "cadeira" in f_type:
        project_data = generate_krat_chair_3d()
    elif "nicho" in f_type:
        project_data = generate_niche_3d(width=width, height=height, depth=depth, thickness=thickness)
    elif "estante" in f_type or "livro" in f_type:
        project_data = generate_bookshelf_3d(width=width, height=height, depth=depth, thickness=thickness, shelves_count=shelves)
    else:
        project_data = generate_cabinet_3d(width=width, height=height, depth=depth, thickness=thickness, doors=doors, shelves=shelves)

    save_current_project(project_data)

    tools = project_data.get("tools", {})
    guide = project_data.get("assembly_guide", {})

    md_lines: List[str] = []
    md_lines.append(f"# Manual de Montagem: {project_data['title']}")
    md_lines.append(f"**Dimensões:** {project_data['dimensions']} | **Dificuldade:** {guide.get('difficulty', 'Média')} | **Tempo Estimado:** {guide.get('estimated_time_hours', 2)}h\n")
    
    md_lines.append("## 1. Ferramentas Necessárias")
    md_lines.append("### 🧰 Essenciais:")
    for t in tools.get("essential_tools", []):
        md_lines.append(f"- **{t['name']}** ({t['spec']}): {t['why']}")

    if tools.get("optional_tools"):
        md_lines.append("\n### ⚙️ Opcionais / Recomendadas:")
        for t in tools.get("optional_tools", []):
            md_lines.append(f"- **{t['name']}** ({t['spec']}): {t['why']}")

    if tools.get("safety_equipment"):
        md_lines.append("\n### 🛡️ Equipamentos de Proteção (EPIs):")
        for s in tools.get("safety_equipment", []):
            md_lines.append(f"- **{s['item']}**: {s['reason']}")

    md_lines.append("\n## 2. Roteiro Passo a Passo de Montagem")
    for phase in guide.get("phases", []):
        md_lines.append(f"\n### Fase {phase['phase_number']}: {phase['title']}")
        if phase.get("description"):
            md_lines.append(f"*{phase['description']}*\n")
        for step in phase.get("steps", []):
            md_lines.append(f"- [ ] {step}")
        if phase.get("tips"):
            md_lines.append(f"> 💡 **Dica de Marceneiro:** {phase['tips']}")

    markdown_text = "\n".join(md_lines)

    return {
        "status": "success",
        "project_title": project_data["title"],
        "dimensions": project_data["dimensions"],
        "estimated_time_hours": guide.get("estimated_time_hours", 2),
        "difficulty": guide.get("difficulty", "Média"),
        "total_phases": len(guide.get("phases", [])),
        "tools": tools,
        "assembly_guide": guide,
        "markdown_manual": markdown_text,
    }


def main() -> None:
    """Ponto de entrada para execução via stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
