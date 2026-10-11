# Simple MCP Server (Python)

A minimal MCP server that exposes two tools backed by REST APIs:

- `get_client(client_id)` → `GET /clients/{client_id}`
- `get_invoice(invoice_id)` → `GET /invoices/{invoice_id}`

The URLs are examples. Replace them with your real API endpoints before using this with real data.

## Requirements

- Python 3.10+
- An MCP-compatible client for actually using the tools

## Setup

```bash
python -m venv .venv
```

Activate the environment:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.venv\\Scripts\\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables by copying `.env.example` to `.env` and setting your API URLs and token. This minimal example does not automatically load `.env`; export the variables in your shell, or add `python-dotenv` and `load_dotenv()` if you prefer.

**macOS / Linux**
```bash
export CLIENTS_API_URL="https://your-api.example.com"
export INVOICES_API_URL="https://your-api.example.com"
export API_TOKEN="your-token"
python server.py
```

**Windows PowerShell**
```powershell
$env:CLIENTS_API_URL = "https://your-api.example.com"
$env:INVOICES_API_URL = "https://your-api.example.com"
$env:API_TOKEN = "your-token"
python server.py
```

`server.py` uses MCP's `stdio` transport. It is normally launched by an MCP client, not used as a regular web server. To inspect and test it during development, you can use the MCP Inspector via the MCP CLI:

```bash
mcp dev server.py
```

If your installed SDK version does not provide `mcp dev`, consult the Python SDK documentation for the current Inspector command.

## Example upstream API contract

This sample expects endpoints that return JSON:

```text
GET https://your-api.example.com/clients/123
GET https://your-api.example.com/invoices/INV-2026-001
```

If your APIs use different paths, authentication, or response formats, edit `server.py`.

## Add another API tool

Add an `@mcp.tool()` function with a clear name, a helpful docstring, typed arguments, and a call to the appropriate API. Avoid exposing secrets as tool arguments.

## Security notes

- Never commit `.env` or real API tokens.
- Use read-only credentials for read-only tools.
- Add authorization checks before exposing sensitive customer or invoice data.
- Treat tool arguments as untrusted input and validate them.
- Add retries/rate limits only where appropriate for the upstream API.
