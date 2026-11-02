"""Teste de fluxo de projeto completo: Armário aéreo de 2 portas."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.leo_client import LeoMadeirasClient
from src.rules import recommend_hardware


async def simulate_aerial_cabinet_project() -> None:
    print("==================================================")
    print("SIMULANDO PROJETO: Armario Aereo 800L x 600A x 350P")
    print("Material: MDF Branco 15mm | 2 Portas de Giro")
    print("==================================================")

    # 1. Decomposição de Peças (BOM)
    # Medidas externas: 800 x 600 x 350 mm
    # Laterais abraçam tampo e base:
    # Laterais: 2x (600 x 350 x 15mm)
    # Tampo e Base: 2x (770 x 350 x 15mm) [800 - 30mm]
    # Portas: 2x (596 x 396 x 15mm)
    pieces = [
        {"nome": "Lateral Direita/Esquerda", "qtd": 2, "c": 600, "l": 350, "esp": 15},
        {"nome": "Tampo e Base", "qtd": 2, "c": 770, "l": 350, "esp": 15},
        {"nome": "Portas", "qtd": 2, "c": 596, "l": 396, "esp": 15},
    ]

    print("\n1. Lista de Corte Calculada:")
    for p in pieces:
        print(f" - {p['qtd']}x {p['nome']}: {p['c']} x {p['l']} x {p['esp']} mm")

    # 2. Metragem de Fita de Borda
    # Portas (4 faces): 2 * 2 * (0.596 + 0.396) = 3.97m
    # Caixaria (frontal): 2 * 0.600 + 2 * 0.770 = 2.74m
    total_edge_m = round(3.97 + 2.74, 2)
    print(f"\n2. Metragem Linear de Fita de Borda: {total_edge_m} m")

    # 3. Kit de Ferragens
    kit = recommend_hardware(
        furniture_type="armario aereo",
        pieces_count=4,
        doors=2,
        door_height_mm=596.0,
        drawers=0,
        linear_edge_meters=total_edge_m,
        sheet_thickness_mm=15,
    )

    print("\n3. Kit de Ferragens Recomendado:")
    for item in kit["hardware_kit"]:
        print(f" - [{item['category']}] {item['item']}: {item['suggested_quantity']} {item['unit']}")

    # 4. Cotação na Leo Madeiras
    client = LeoMadeirasClient()
    print("\n4. Consultando Itens na Leo Madeiras via API:")

    # Buscar MDF Branco 15mm
    mdf_res = await client.search_products(query="MDF Branco", thickness="15mm", limit=2)
    mdf_prod = mdf_res["products"][0] if mdf_res["products"] else None
    if mdf_prod:
        print(f" - Chapa MDF: {mdf_prod['name']} | R$ {mdf_prod['price']} | {mdf_prod['link']}")

    # Buscar Fita de Borda
    edge_res = await client.search_products(query="Fita de Borda Branca 22mm", limit=2)
    edge_prod = edge_res["products"][0] if edge_res["products"] else None
    if edge_prod:
        print(f" - Fita de Borda: {edge_prod['name']} | R$ {edge_prod['price']} | {edge_prod['link']}")

    # Buscar Dobradiças
    hinge_res = await client.search_products(query="Dobradiça Caneco 35mm Amortecedor", limit=2)
    hinge_prod = hinge_res["products"][0] if hinge_res["products"] else None
    if hinge_prod:
        print(f" - Dobradiças: {hinge_prod['name']} | R$ {hinge_prod['price']} | {hinge_prod['link']}")

    print("\nFLUXO COMPLETO EXECUTADO COM SUCESSO! PROJETO PRONTO PARA MONTAGEM.")


if __name__ == "__main__":
    asyncio.run(simulate_aerial_cabinet_project())
