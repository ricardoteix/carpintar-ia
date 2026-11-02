"""Teste unitário do otimizador de plano de corte 2D."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cutlist_optimizer import optimize_cutting_plan


def test_cutting_optimizer() -> None:
    print("=== Testando Otimizador de Plano de Corte 2D ===")

    # Teste 1: Armário pequeno em 1 chapa de MDF 2750 x 1830 mm
    pieces = [
        {"name": "Lateral Direita", "length": 600, "width": 350, "quantity": 1},
        {"name": "Lateral Esquerda", "length": 600, "width": 350, "quantity": 1},
        {"name": "Tampo Superior", "length": 770, "width": 350, "quantity": 1},
        {"name": "Base Inferior", "length": 770, "width": 350, "quantity": 1},
        {"name": "Porta", "length": 596, "width": 396, "quantity": 2},
    ]

    result = optimize_cutting_plan(pieces=pieces, sheet_width=2750, sheet_height=1830)

    print(f"Chapas necessárias: {result['sheets_needed']}")
    print(f"Total de peças posicionadas: {result['total_pieces_count']}")
    print(f"Aproveitamento da chapa: {result['overall_utilization_percent']}%")
    print(f"Sobras aproveitáveis encontradas: {len(result['usable_offcuts'])}")

    assert result["sheets_needed"] == 1
    assert result["total_pieces_count"] == 6
    assert result["overall_utilization_percent"] > 0
    assert len(result["usable_offcuts"]) > 0

    print("\n[OK] Teste 1 (Armario em Chapa Padrao) passou!")

    # Teste 2: Projeto maior que exige múltiplas chapas ou tamanho menor
    # 2 painéis de Pinus 2400 x 300 mm com várias ripas
    krat_pieces = [
        {"name": "Pe Frontal", "length": 580, "width": 95, "quantity": 2},
        {"name": "Pe Traseiro", "length": 540, "width": 95, "quantity": 2},
        {"name": "Braco", "length": 600, "width": 95, "quantity": 2},
        {"name": "Travessa Inferior", "length": 580, "width": 95, "quantity": 2},
        {"name": "Ripa Assento", "length": 500, "width": 95, "quantity": 4},
        {"name": "Ripa Encosto", "length": 500, "width": 95, "quantity": 3},
    ]

    # Painel de Pinus: 2400 x 300 mm
    krat_result = optimize_cutting_plan(
        pieces=krat_pieces,
        sheet_width=2400,
        sheet_height=300,
        margin=5,
        kerf=3,
        allow_rotation=True,
    )

    print(f"\nKrat Chair em Paineis de Pinus (2400x300mm):")
    print(f"Paineis necessários: {krat_result['sheets_needed']}")
    print(f"Total de peças: {krat_result['total_pieces_count']}")
    print(f"Aproveitamento geral: {krat_result['overall_utilization_percent']}%")

    assert krat_result["sheets_needed"] >= 2
    assert krat_result["total_pieces_count"] == 15

    print("\n[OK] Teste 2 (Krat Chair em Paineis de Pinus) passou!")
    print("\nTODOS OS TESTES DE CORTE PASSARAM COM SUCESSO!")


if __name__ == "__main__":
    test_cutting_optimizer()
