"""Otimizador de Plano de Corte 2D para Marcenaria (Guillotine Bin Packing)."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Rect:
    """Retângulo representando espaço livre ou peça posicionada na chapa."""
    x: float
    y: float
    width: float
    height: float


@dataclass
class PlacedPiece:
    """Peça já posicionada na chapa."""
    id: str
    name: str
    x: float
    y: float
    length: float
    width: float
    rotated: bool


class Sheet:
    """Representa uma chapa individual e seus espaços livres/ocupados."""

    def __init__(
        self,
        sheet_index: int,
        total_width: float,
        total_height: float,
        margin: float,
    ) -> None:
        self.sheet_index = sheet_index
        self.total_width = total_width
        self.total_height = total_height
        self.margin = margin

        # Área útil inicial após o refile
        usable_w = total_width - (2 * margin)
        usable_h = total_height - (2 * margin)
        self.free_rectangles: List[Rect] = [
            Rect(x=margin, y=margin, width=usable_w, height=usable_h)
        ]
        self.placed_pieces: List[PlacedPiece] = []

    def can_fit(
        self,
        rect: Rect,
        piece_w: float,
        piece_h: float,
    ) -> bool:
        """Verifica se uma dimensão cabe dentro do retângulo livre."""
        return rect.width >= piece_w and rect.height >= piece_h

    def place_piece(
        self,
        piece_id: str,
        name: str,
        length: float,
        width: float,
        can_rotate: bool,
        kerf: float,
    ) -> Optional[PlacedPiece]:
        """Tenta posicionar a peça nesta chapa usando a heurística Best Short Side Fit."""
        best_rect_idx: Optional[int] = None
        best_rotated = False
        best_short_fit = float("inf")

        for idx, free_rect in enumerate(self.free_rectangles):
            # Orientação Normal: length no eixo X, width no eixo Y
            if self.can_fit(free_rect, length, width):
                short_side = min(free_rect.width - length, free_rect.height - width)
                if short_side < best_short_fit:
                    best_short_fit = short_side
                    best_rect_idx = idx
                    best_rotated = False

            # Orientação Rotacionada (90 graus): width no eixo X, length no eixo Y
            if can_rotate and self.can_fit(free_rect, width, length):
                short_side = min(free_rect.width - width, free_rect.height - length)
                if short_side < best_short_fit:
                    best_short_fit = short_side
                    best_rect_idx = idx
                    best_rotated = True

        if best_rect_idx is None:
            return None

        # Recupera o retângulo livre escolhido
        target_rect = self.free_rectangles.pop(best_rect_idx)

        placed_w = width if best_rotated else length
        placed_h = length if best_rotated else width

        placed = PlacedPiece(
            id=piece_id,
            name=name,
            x=round(target_rect.x, 1),
            y=round(target_rect.y, 1),
            length=round(placed_w, 1),
            width=round(placed_h, 1),
            rotated=best_rotated,
        )
        self.placed_pieces.append(placed)

        # Divisão de Guilhotina (Shorter Axis Split) considerando o kerf
        rem_w = target_rect.width - placed_w - kerf
        rem_h = target_rect.height - placed_h - kerf

        # Divide o espaço residual em dois retângulos menores
        if placed_w <= placed_h:
            # Corte horizontal primeiro
            if rem_w > 0:
                self.free_rectangles.append(
                    Rect(x=target_rect.x + placed_w + kerf, y=target_rect.y, width=rem_w, height=placed_h)
                )
            if target_rect.height - placed_h - kerf > 0:
                self.free_rectangles.append(
                    Rect(x=target_rect.x, y=target_rect.y + placed_h + kerf, width=target_rect.width, height=rem_h)
                )
        else:
            # Corte vertical primeiro
            if rem_h > 0:
                self.free_rectangles.append(
                    Rect(x=target_rect.x, y=target_rect.y + placed_h + kerf, width=placed_w, height=rem_h)
                )
            if target_rect.width - placed_w - kerf > 0:
                self.free_rectangles.append(
                    Rect(x=target_rect.x + placed_w + kerf, y=target_rect.y, width=rem_w, height=target_rect.height)
                )

        return placed


def optimize_cutting_plan(
    pieces: List[Dict[str, Any]],
    sheet_width: float = 2750.0,
    sheet_height: float = 1830.0,
    kerf: float = 4.0,
    margin: float = 10.0,
    allow_rotation: bool = True,
    min_offcut_dimension: float = 100.0,
) -> Dict[str, Any]:
    """Calcula a distribuição otimizada de peças de corte em chapas industriais.

    Args:
        pieces: Lista de peças, ex: [{'name': 'Lateral', 'length': 600, 'width': 350, 'quantity': 2, 'can_rotate': True}]
        sheet_width: Comprimento total da chapa bruta em mm (padrão 2750mm)
        sheet_height: Largura total da chapa bruta em mm (padrão 1830mm)
        kerf: Espessura do corte da serra em mm (padrão 4mm)
        margin: Refile em cada borda da chapa em mm (padrão 10mm)
        allow_rotation: Permite girar peças 90 graus por padrão (se False respeita sentido de veio)
        min_offcut_dimension: Dimensão mínima para considerar um retalho aproveitável
    """
    # 1. Desmembrar quantidades em itens individuais
    flat_items: List[Dict[str, Any]] = []
    item_counter = 1
    for p in pieces:
        qtd = max(1, int(p.get("quantity", 1)))
        length = float(p.get("length", 0))
        width = float(p.get("width", 0))
        name = p.get("name", f"Peça {item_counter}")
        p_rotate = p.get("can_rotate", allow_rotation)

        for i in range(qtd):
            flat_items.append({
                "id": f"P{item_counter}_{i+1}",
                "name": f"{name} (#{i+1})" if qtd > 1 else name,
                "length": max(length, width),  # normaliza maior dimensão como length
                "width": min(length, width),
                "can_rotate": p_rotate,
                "area": length * width,
            })
        item_counter += 1

    # 2. Ordenar decrescente por área (First Fit Decreasing)
    flat_items.sort(key=lambda x: (x["area"], x["length"]), reverse=True)

    sheets: List[Sheet] = []

    for item in flat_items:
        placed = False
        # Tenta encaixar nas chapas já existentes
        for sheet in sheets:
            if sheet.place_piece(
                piece_id=item["id"],
                name=item["name"],
                length=item["length"],
                width=item["width"],
                can_rotate=item["can_rotate"],
                kerf=kerf,
            ):
                placed = True
                break

        # Se não coube em nenhuma, abre uma nova chapa
        if not placed:
            new_sheet = Sheet(
                sheet_index=len(sheets) + 1,
                total_width=sheet_width,
                total_height=sheet_height,
                margin=margin,
            )
            success = new_sheet.place_piece(
                piece_id=item["id"],
                name=item["name"],
                length=item["length"],
                width=item["width"],
                can_rotate=item["can_rotate"],
                kerf=kerf,
            )
            if not success:
                return {
                    "error": (
                        f"A peça '{item['name']}' ({item['length']}x{item['width']}mm) "
                        f"é maior que a área útil da chapa ({sheet_width - 2*margin}x{sheet_height - 2*margin}mm)."
                    ),
                    "sheets_needed": 0,
                }
            sheets.append(new_sheet)

    # 3. Calcular métricas e aproveitamento
    total_sheet_area = len(sheets) * (sheet_width * sheet_height)
    total_pieces_area = sum(item["area"] for item in flat_items)
    utilization_pct = round((total_pieces_area / total_sheet_area) * 100, 1) if total_sheet_area > 0 else 0.0

    sheets_summary: List[Dict[str, Any]] = []
    total_usable_offcuts: List[Dict[str, Any]] = []

    for s in sheets:
        pieces_data = [
            {
                "id": p.id,
                "name": p.name,
                "x_mm": p.x,
                "y_mm": p.y,
                "length_mm": p.length,
                "width_mm": p.width,
                "rotated": p.rotated,
            }
            for p in s.placed_pieces
        ]

        # Retalhos que sobraram nesta chapa
        offcuts = [
            {
                "sheet": s.sheet_index,
                "x_mm": round(r.x, 1),
                "y_mm": round(r.y, 1),
                "width_mm": round(r.width, 1),
                "height_mm": round(r.height, 1),
                "area_m2": round((r.width * r.height) / 1_000_000, 3),
            }
            for r in s.free_rectangles
            if r.width >= min_offcut_dimension and r.height >= min_offcut_dimension
        ]
        total_usable_offcuts.extend(offcuts)

        s_piece_area = sum(p.length * p.width for p in s.placed_pieces)
        s_utilization = round((s_piece_area / (sheet_width * sheet_height)) * 100, 1)

        sheets_summary.append({
            "sheet_number": s.sheet_index,
            "pieces_count": len(pieces_data),
            "utilization_percent": s_utilization,
            "placed_pieces": pieces_data,
            "usable_offcuts_count": len(offcuts),
        })

    return {
        "sheets_needed": len(sheets),
        "total_pieces_count": len(flat_items),
        "sheet_dimensions_mm": {"width": sheet_width, "height": sheet_height},
        "kerf_mm": kerf,
        "margin_mm": margin,
        "total_pieces_area_m2": round(total_pieces_area / 1_000_000, 2),
        "total_sheets_area_m2": round(total_sheet_area / 1_000_000, 2),
        "overall_utilization_percent": utilization_pct,
        "waste_percent": round(100.0 - utilization_pct, 1),
        "sheets": sheets_summary,
        "usable_offcuts": total_usable_offcuts,
    }
