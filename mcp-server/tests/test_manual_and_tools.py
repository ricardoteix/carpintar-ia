"""Testes automatizados para dedução de ferramentas e geração do manual de montagem."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rules import recommend_tools
from src.project_3d import generate_krat_chair_3d, generate_cabinet_3d
from src.server import generate_assembly_manual


def test_recommend_tools() -> None:
    print("=== 1. Testando Dedução de Ferramentas e EPIs ===")

    # 1. Cadeira Krat (madeira maciça, sem portas)
    krat_tools = recommend_tools("krat")
    assert krat_tools["is_wood_solid"] is True
    essential_names = [t["name"] for t in krat_tools["essential_tools"]]
    assert "Parafusadeira / Furadeira" in essential_names
    assert "Broca Piloto 3.0 mm com Escareador" in essential_names
    assert "Esquadro Combinado Metálico" in essential_names
    assert "Grampos Sargentos (2 a 4 unidades)" in essential_names

    # 2. Armário com portas (deve exigir broca caneco 35mm)
    cab_tools = recommend_tools("armario", doors=2)
    cab_essential_names = [t["name"] for t in cab_tools["essential_tools"]]
    assert any("35" in name for name in cab_essential_names), "Fresa caneco 35mm deve ser recomendada para portas"

    # 3. Marcenaria completa com cortes próprios
    shop_tools = recommend_tools("armario", cuts_in_shop=True)
    optional_names = [t["name"] for t in shop_tools["optional_tools"]]
    assert any("Serra Circular" in name for name in optional_names)
    assert any("Refilador de Fita" in name for name in optional_names)

    # 4. EPIs obrigatórios
    safety_items = [s["item"] for s in krat_tools["safety_equipment"]]
    assert any("Óculos" in item for item in safety_items)
    assert any("Máscara" in item for item in safety_items)

    print("[OK] Testes de dedução de ferramentas passaram!")


def test_assembly_manual_generation() -> None:
    print("=== 2. Testando Geração do Manual de Montagem ===")

    # 1. Modelo da Cadeira Krat
    krat = generate_krat_chair_3d()
    assert "assembly_guide" in krat
    guide = krat["assembly_guide"]
    assert guide["estimated_time_hours"] > 0
    assert len(guide["phases"]) == 5  # 5 fases detalhadas
    assert "Módulo do Assento" in guide["phases"][2]["title"]

    # 2. Tool MCP generate_assembly_manual
    res = generate_assembly_manual(furniture_type="krat")
    assert res["status"] == "success"
    assert res["project_title"] == "Cadeira Krat (Gerrit Rietveld, 1934)"
    assert res["total_phases"] == 5
    assert len(res["markdown_manual"]) > 200
    assert "Fase 1: Conferência e Pré-Furação" in res["markdown_manual"]

    print("[OK] Testes de geração do manual de montagem passaram!")


if __name__ == "__main__":
    test_recommend_tools()
    test_assembly_manual_generation()
    print("\nTODOS OS TESTES DE MANUAL E FERRAMENTAS PASSARAM COM SUCESSO!")
