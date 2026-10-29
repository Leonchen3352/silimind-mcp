# Connect your AI assistant to SiliMind

SiliMind speaks **MCP** (Model Context Protocol) — the standard way for AI assistants to use external tools.

## What this means for you

Your AI assistant can now directly read (and safely write to) your SiliMind CRM:

- **Claude Desktop** — ask Claude about your deals, customers, tasks
- **ChatGPT** — query your pipeline through custom GPTs
- **Cursor / any MCP client** — build your own AI workflows on SiliMind data

## What your AI can do

| | |
|---|---|
| 🔍 **Search customers** | "Find all contacts at Acme Corp" |
| 📊 **Check deals** | "What's in my follow-up pipeline?" |
| 📅 **View calendar** | "What's on my schedule tomorrow?" |
| 📝 **Create tasks** | "Add a follow-up task for John" (requires your approval in SiliMind) |
| 🧠 **Query anything** | Natural language questions about your allowed data |

## How to connect

**Step 1** — Get your MCP token: SiliMind → Settings → MCP Access → Generate

**Step 2** — Add to Claude Desktop:
```json
{
  "mcpServers": {
    "silimind": {
      "command": "python",
      "args": ["-m", "silimind_mcp.stdio_bridge"],
      "env": {
        "SILIMIND_URL": "https://agent.silimind.net",
        "SILIMIND_TOKEN": "smcp_your_token"
      }
    }
  }
}
```

**Step 3** — Ask away: *"Hey Claude, what are my top deals this week?"*

## Security first

- 🔒 Per-token permissions (readonly / readwrite)
- 🔒 Tenant isolation — your AI sees only your data
- 🔒 Rate-limited and fully audit-logged
- 🔒 **Writes need your approval** — AI proposes, you approve inside SiliMind

**GitHub**: [github.com/Leonchen3352/silimind-mcp](https://github.com/Leonchen3352/silimind-mcp)
