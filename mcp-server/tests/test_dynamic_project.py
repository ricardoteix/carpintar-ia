"""Teste do gerador universal e do modelo corrigido da Cadeira Krat."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.project_3d import (
    generate_krat_chair_3d,
    generate_cabinet_3d,
    generate_bookshelf_3d,
    generate_niche_3d,
    save_current_project,
)


def test_universal_generators() -> None:
    print("=== 1. Testando Cadeira Krat Oficial (18 peças) ===")
    krat = generate_krat_chair_3d()
    print(f"Título: {krat['title']} | Peças: {len(krat['pieces'])}")
    assert len(krat["pieces"]) == 18  # 18 peças oficiais do DAE e manual montagem-krat.md
    piece_names = [p["name"] for p in krat["pieces"]]
    assert "Lateral Esquerda - Apoio de Braço" in piece_names
    assert "Assento - Tábua Central" in piece_names
    assert "Encosto - Tábua Central" in piece_names
    print("[OK] Cadeira Krat corrigida com sucesso!")

    print("\n=== 2. Testando Outros Tipos de Móveis ===")
    estante = generate_bookshelf_3d(width=900, height=1900, depth=320, shelves_count=5)
    assert len(estante["pieces"]) >= 9
    print(f"[OK] Estante gerada com {len(estante['pieces'])} peças.")

    nicho = generate_niche_3d(width=500, height=350, depth=180)
    assert len(nicho["pieces"]) == 5
    print(f"[OK] Nicho gerado com {len(nicho['pieces'])} peças.")

    print("\n=== 3. Testando Salvamento em viewer/current_project.js ===")
    paths = save_current_project(krat)
    print(f"Salvo em: {paths['js_path']} e {paths['json_path']}")
    assert os.path.exists(paths["js_path"])
    assert os.path.exists(paths["json_path"])

    with open(paths["js_path"], "r", encoding="utf-8") as f:
        content = f.read()
        assert "window.CURRENT_PROJECT =" in content
        assert "Cadeira Krat" in content

    print("[OK] current_project.js criado e verificado com sucesso!")
    print("\nTODOS OS TESTES PASSARAM COM SUCESSO!")


if __name__ == "__main__":
    test_universal_generators()
