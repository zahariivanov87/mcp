"""Minimal MCP server exposing two example business API tools."""

import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Business APIs")

# Replace these with your real API base URLs.
CLIENTS_API_URL = os.getenv("CLIENTS_API_URL", "https://api.example.com")
INVOICES_API_URL = os.getenv("INVOICES_API_URL", "https://api.example.com")
API_TOKEN = os.getenv("API_TOKEN", "")


async def api_get(base_url: str, path: str) -> dict:
    """Call an upstream API and return its JSON response."""
    headers = {}
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{base_url.rstrip('/')}/{path.lstrip('/')}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_client(client_id: str) -> dict:
    """Get a client's details by client ID, such as 123."""
    return await api_get(CLIENTS_API_URL, f"clients/{client_id}")


@mcp.tool()
async def get_invoice(invoice_id: str) -> dict:
    """Get invoice details by invoice ID, such as INV-2026-001."""
    return await api_get(INVOICES_API_URL, f"invoices/{invoice_id}")


if __name__ == "__main__":
    # stdio transport: intended to be launched by an MCP-compatible client.
    mcp.run(transport="stdio")
