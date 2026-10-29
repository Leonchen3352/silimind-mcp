"""Stdio-to-HTTP bridge for MCP clients that only speak stdio (e.g. Claude Desktop).

Reads JSON-RPC from stdin, forwards to SiliMind /mcp/external, writes responses
to stdout. This lets Claude Desktop / Cursor connect without a native HTTP
transport.

Usage in Claude Desktop config (~/.claude/claude_desktop_config.json):
  "mcpServers": {
    "silimind": {
      "command": "python",
      "args": ["-m", "silimind_mcp.stdio_bridge"],
      "env": {
        "SILIMIND_URL": "https://agent.silimind.net",
        "SILIMIND_TOKEN": "your-mcp-token"
      }
    }
  }
"""
import json
import os
import sys
import urllib.request
import urllib.error

PROTOCOL_VERSION = "2025-03-26"

def forward(payload, endpoint, token):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "MCP-Protocol-Version": PROTOCOL_VERSION,
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"jsonrpc": "2.0", "id": payload.get("id"),
                "error": {"code": e.code, "message": e.read().decode()[:300]}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": payload.get("id"),
                "error": {"code": -32603, "message": str(e)}}

def main():
    url = os.environ.get("SILIMIND_URL", "").rstrip("/")
    token = os.environ.get("SILIMIND_TOKEN", "")
    if not url or not token:
        print("Set SILIMIND_URL and SILIMIND_TOKEN", file=sys.stderr)
        sys.exit(1)
    endpoint = url + "/mcp/external"
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        result = forward(payload, endpoint, token)
        sys.stdout.write(json.dumps(result) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
