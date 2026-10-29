# SiliMind MCP Server

Connect **Claude Desktop / ChatGPT / Cursor** (any MCP-compatible client) to your **SiliMind CRM**.

Ask your AI assistant things like:
- *"Show me my open deals this week"*
- *"What's on my calendar tomorrow?"*
- *"Create a follow-up task for Acme Corp"*

Your AI talks to SiliMind through read-only (and opt-in write-proposal) MCP tools — with your per-user permissions, tenant isolation, and full audit trail.

## What it does

SiliMind exposes an **external MCP gateway** at `/mcp/external` (Streamable HTTP, JSON-RPC 2.0). This package provides:

1. **Python client library** (`silimind_mcp.SilimindMCPClient`) — for building custom integrations
2. **CLI** (`python -m silimind_mcp.server`) — list tools, call a tool from terminal
3. **Stdio bridge** (`python -m silimind_mcp.stdio_bridge`) — for clients that only speak stdio (Claude Desktop, Cursor)

## Available tools (read-only)

| Tool | Description |
|---|---|
| `search_customers` | Search customers (respects your permissions) |
| `get_customer_detail` | Get full customer profile |
| `list_deals` / `get_deal` | Browse opportunities |
| `dashboard_summary` | Your business overview |
| `query_data` | Ask questions in natural language (SELECT-only, whitelisted tables) |
| `list_contracts` / `get_contract` | View contracts |
| `list_tasks` | Your task list |
| `list_calendar` | Merged calendar view |
| `list_outbound_jobs` | Outbound prospecting progress |

### Write-proposal tools (opt-in, `readwrite` scope tokens only)

Write tools **never write directly** — they create a proposal that you approve inside SiliMind:

| Tool | Description |
|---|---|
| `crm_create_contact` | Propose creating a new contact |
| `crm_create_deal` | Propose creating a new deal |
| `create_task` | Propose creating a task |
| `crm_add_interaction` | Propose adding a timeline interaction |

> Proposals expire after 24h if not approved. Nothing touches your CRM without your explicit approval.

## Setup

### 1. Get your MCP token

In SiliMind: **Settings → MCP Access** → Generate token (`readonly` or `readwrite` scope).

### 2. Configure your client

**Claude Desktop** (`~/.claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "silimind": {
      "command": "python",
      "args": ["-m", "silimind_mcp.stdio_bridge"],
      "env": {
        "SILIMIND_URL": "https://agent.silimind.net",
        "SILIMIND_TOKEN": "smcp_your_token_here"
      }
    }
  }
}
```

**Any HTTP MCP client**: point it at `https://agent.silimind.net/mcp/external` with header `Authorization: Bearer smcp_...`.

**CLI quick test**:
```bash
pip install silimind-mcp
export SILIMIND_URL=https://agent.silimind.net
export SILIMIND_TOKEN=smcp_...
python -m silimind_mcp.server list
```

## Security

- Per-token permissions (readonly / readwrite scope)
- Tenant isolation & row-level security enforced server-side
- Rate limiting (per-token per-minute + daily quota)
- Every call audit-logged
- Write operations require human approval inside SiliMind

## Install

```bash
pip install silimind-mcp
```
Or from source:
```bash
git clone https://github.com/Leonchen3352/silimind-mcp.git
cd silimind-mcp
pip install -e .
```

## License

Apache-2.0
