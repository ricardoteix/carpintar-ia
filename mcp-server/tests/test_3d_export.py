"""Teste de exportação de dados para o visualizador 3D."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.project_3d import generate_cabinet_3d, export_project_to_file


def test_3d_generation() -> None:
    print("=== Testando Gerador de Modelo 3D ===")

    project = generate_cabinet_3d(width=900, height=700, depth=400, thickness=18, doors=2, shelves=0)
    assert project["title"] == "Armário (900x700x400mm)"
    assert len(project["pieces"]) == 7  # 2 laterais + tampo + base + fundo + 2 portas

    for p in project["pieces"]:
        print(f" - Peça: {p['name']} | Tamanho: {p['size']} | Pos: {p['pos']} | Dir: {p['dir']}")
        assert len(p["size"]) == 3
        assert len(p["pos"]) == 3
        assert len(p["dir"]) == 3

    # Testa salvar arquivo JSON
    saved_file = export_project_to_file(project, filename="test_cabinet.json")
    print(f"\nArquivo salvo com sucesso em: {saved_file}")
    assert os.path.exists(saved_file)

    print("\nTODOS OS TESTES DO VISUALIZADOR 3D PASSARAM!")


if __name__ == "__main__":
    test_3d_generation()
