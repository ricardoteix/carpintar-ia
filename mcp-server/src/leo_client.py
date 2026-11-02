"""Cliente HTTP assíncrono para os endpoints públicos da Leo Madeiras."""

from typing import Any, Dict, List, Optional
import httpx


LEO_BASE_URL = "https://www.leomadeiras.com.br"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
}


class LeoMadeirasClient:
    """Cliente para consulta da API de busca e catálogo da Leo Madeiras."""

    def __init__(self, timeout: float = 15.0) -> None:
        self.timeout = timeout

    async def search_products(
        self,
        query: str,
        thickness: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
        sort: str = "relevance",
    ) -> Dict[str, Any]:
        """Busca produtos na Leo Madeiras pelo termo, suportando espessura opcional."""
        full_query = query.strip()
        if thickness and thickness.lower() not in full_query.lower():
            full_query = f"{full_query} {thickness}"

        from_idx = max(0, offset)
        to_idx = from_idx + max(1, min(limit, 50)) - 1

        url = f"{LEO_BASE_URL}/api/search"
        params = {
            "q": full_query,
            "sort": sort,
            "from": str(from_idx),
            "to": str(to_idx),
        }

        try:
            async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            return {
                "error": f"Erro de comunicação com Leo Madeiras: {str(exc)}",
                "products": [],
                "total": 0,
            }
        except Exception as exc:
            return {
                "error": f"Erro inesperado ao consultar produtos: {str(exc)}",
                "products": [],
                "total": 0,
            }

        raw_products = data.get("products", [])
        total = data.get("total", len(raw_products))

        products: List[Dict[str, Any]] = []
        for p in raw_products:
            slug = p.get("slug", "")
            link = f"{LEO_BASE_URL}/{slug}/p" if slug else ""
            products.append({
                "id": str(p.get("id", "")),
                "name": p.get("name", ""),
                "price": p.get("price"),
                "list_price": p.get("listPrice"),
                "brand": p.get("brand", ""),
                "category": p.get("category", ""),
                "stock": p.get("stock", 0),
                "link": link,
            })

        # Extrair facetas úteis de forma resumida
        facets_summary: Dict[str, List[str]] = {}
        for facet in data.get("facets", []):
            f_name = facet.get("name")
            if f_name in ["Espessura", "Dimensões", "Faces", "Cor"]:
                values = [v.get("name") for v in facet.get("values", [])[:8] if v.get("name")]
                if values:
                    facets_summary[f_name] = values

        return {
            "query": full_query,
            "total_found": total,
            "returned_count": len(products),
            "products": products,
            "available_facets": facets_summary,
        }

    async def get_suggestions(self, query: str) -> Dict[str, Any]:
        """Obtém termos sugeridos e produtos rápidos para o termo informado."""
        url = f"{LEO_BASE_URL}/api/suggestions"
        params = {"q": query.strip()}

        try:
            async with httpx.AsyncClient(headers=DEFAULT_HEADERS, timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            return {
                "error": f"Erro de comunicação com Leo Madeiras: {str(exc)}",
                "terms": [],
                "products": [],
            }
        except Exception as exc:
            return {
                "error": f"Erro inesperado ao buscar sugestões: {str(exc)}",
                "terms": [],
                "products": [],
            }

        terms = data.get("terms", [])
        raw_products = data.get("products", [])
        products = []
        for p in raw_products:
            slug = p.get("slug", "")
            products.append({
                "id": str(p.get("id", "")),
                "name": p.get("name", ""),
                "price": p.get("price"),
                "brand": p.get("brand", ""),
                "link": f"{LEO_BASE_URL}/{slug}/p" if slug else "",
            })

        return {
            "query": query,
            "suggested_terms": terms,
            "suggested_products": products,
        }
