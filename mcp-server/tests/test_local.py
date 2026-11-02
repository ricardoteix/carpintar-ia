"""Script de teste de ponta a ponta para validação do MCP e do cliente Leo Madeiras."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.leo_client import LeoMadeirasClient
from src.rules import recommend_hardware


async def run_tests() -> None:
    print("=== 1. Testando Sugestoes ===")
    client = LeoMadeirasClient()
    sugg = await client.get_suggestions("Pinus")
    terms_count = len(sugg.get("suggested_terms", []))
    prod_count = len(sugg.get("suggested_products", []))
    print(f"Sugestoes encontradas: {terms_count} termos, {prod_count} produtos")
    assert terms_count > 0 or prod_count > 0
    print("[OK] Sugestoes OK")

    print("\n=== 2. Testando Busca com Espessura (MDF Branco 15mm) ===")
    res = await client.search_products(query="MDF Branco", thickness="15mm", limit=3)
    print(f"Total encontrado: {res.get('total_found')}, Retornados: {res.get('returned_count')}")
    for p in res.get("products", []):
        print(f" - [{p['id']}] {p['name']} | R$ {p['price']} | Link: {p['link']}")
    assert res.get("returned_count", 0) > 0
    print("[OK] Busca de produtos OK")

    print("\n=== 3. Testando Regras de Kit de Ferragens ===")
    kit = recommend_hardware(
        furniture_type="nicho",
        pieces_count=4,
        doors=0,
        drawers=0,
        linear_edge_meters=2.4,
        sheet_thickness_mm=15,
    )
    print(f"Itens recomendados para nicho: {kit.get('total_items_recommended')}")
    for item in kit.get("hardware_kit", []):
        print(f" - [{item['category']}] {item['item']}: {item['suggested_quantity']} {item['unit']}")
    assert kit.get("total_items_recommended", 0) >= 3
    print("[OK] Kit de ferragens OK")

    print("\nTODOS OS TESTES PASSARAM COM SUCESSO!")


if __name__ == "__main__":
    asyncio.run(run_tests())
