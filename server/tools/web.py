"""Web/API Tools for MCP Server"""
import httpx
from typing import Any, Optional


async def fetch_url(url: str, method: str = "GET") -> dict[str, Any]:
    """Fetch content from a URL"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(method, url)

            return {
                "url": url,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "size": len(response.content)
            }
    except Exception as e:
        return {"error": f"Error fetching URL: {str(e)}"}


async def http_request(
    url: str,
    method: str = "GET",
    headers: Optional[dict] = None,
    body: Optional[str] = None
) -> dict[str, Any]:
    """Make an HTTP request with custom headers and body"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method,
                url,
                headers=headers or {},
                content=body
            )

            return {
                "url": url,
                "method": method,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "size": len(response.content)
            }
    except Exception as e:
        return {"error": f"Error making HTTP request: {str(e)}"}
