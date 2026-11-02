# Carpintaria Leo Madeiras - MCP Server

Servidor MCP (Model Context Protocol) local em Python que expõe ferramentas de busca de produtos, sugestões e cotação de materiais na [Leo Madeiras](https://www.leomadeiras.com.br), além de regras especializadas de cálculo de ferragens e insumos para marcenaria sob medida.

---

## 🛠️ Ferramentas Disponíveis

| Ferramenta | Descrição | Parâmetros Principais |
| :--- | :--- | :--- |
| `search_materials` | Pesquisa produtos na Leo Madeiras com filtros e paginação | `query`, `thickness` (ex: "15mm"), `limit`, `offset` |
| `suggest_terms` | Autocomplete e busca rápida de termos/produtos | `query` |
| `recommend_hardware_kit` | Calcula lista de parafusos, dobradiças, corrediças, fita e fixadores | `furniture_type`, `pieces_count`, `doors`, `drawers`, `linear_edge_meters`, `sheet_thickness_mm` |
| `calculate_cutting_plan` | Otimização 2D de corte (guilhotina) para encaixe em chapas e cálculo de sobras | `pieces`, `sheet_width`, `sheet_height`, `kerf`, `margin`, `allow_rotation` |
| `export_3d_project` | Exporta coordenadas 3D e vetores de explosão para o visualizador web | `furniture_type`, `width`, `height`, `depth`, `thickness`, `doors`, `filename` |

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.10+ (ou [uv](https://docs.astral.sh/uv/))

### Instalação

```bash
cd mcp-server

# Opção 1: Usando uv (rápido e recomendado)
uv venv
uv pip install -r requirements.txt

# Opção 2: Usando venv padrão
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Execução dos Testes Locais

```bash
.venv\Scripts\python tests/test_local.py
```

---

## 🔌 Como Registrar no seu Cliente MCP

### 1. Antigravity / Claude Desktop

No arquivo de configuração de servidores MCP (ex: `claude_desktop_config.json` ou nas configurações do seu cliente):

```json
{
  "mcpServers": {
    "carpintaria-leo-madeiras": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\Github\\carpintaria-mcp\\mcp-server",
        "run",
        "src/server.py"
      ]
    }
  }
}
```

Ou apontando diretamente para o executável Python do ambiente virtual:

```json
{
  "mcpServers": {
    "carpintaria-leo-madeiras": {
      "command": "D:\\Github\\carpintaria-mcp\\mcp-server\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Github\\carpintaria-mcp\\mcp-server\\src\\server.py"
      ]
    }
  }
}
```
