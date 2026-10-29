"""SiliMind MCP Server.

A thin MCP (Model Context Protocol) server that exposes SiliMind CRM tools
to any MCP-compatible client (Claude Desktop, ChatGPT, Cursor, etc.) via
Streamable HTTP (JSON-RPC 2.0).

Configuration (env vars):
  SILIMIND_URL    — Your SiliMind instance (e.g. https://agent.silimind.net)
  SILIMIND_TOKEN  — MCP Bearer token (from SiliMind: Settings → MCP Access)

Run:
  python -m silimind_mcp.server
"""
import json
import os
import sys
import urllib.request
import urllib.error

__all__ = ["SilimindMCPClient", "main"]

PROTOCOL_VERSION = "2025-03-26"
SERVER_INFO = {"name": "silimind-mcp", "version": "0.1.0"}


class SilimindMCPClient:
    """JSON-RPC 2.0 client for SiliMind's external MCP gateway."""

    def __init__(self, base_url: str, token: str, timeout: int = 30):
        self.endpoint = base_url.rstrip("/") + "/mcp/external"
        self.token = token
        self.timeout = timeout

    def call(self, method: str, params=None):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {},
        }
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
                "MCP-Protocol-Version": PROTOCOL_VERSION,
            },
        )
        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:500]
            return {"error": {"code": e.code, "message": body}}


def get_tools(client: SilimindMCPClient):
    resp = client.call("tools/list")
    return resp.get("result", {}).get("tools", [])


def call_tool(client: SilimindMCPClient, name: str, arguments=None):
    resp = client.call("tools/call", {"name": name, "arguments": arguments or {}})
    return resp.get("result", resp)


def main():
    """CLI: list tools or call one. Useful for testing without an MCP client."""
    url = os.environ.get("SILIMIND_URL", "").rstrip("/")
    token = os.environ.get("SILIMIND_TOKEN", "")
    if not url or not token:
        print("Set SILIMIND_URL and SILIMIND_TOKEN env vars.", file=sys.stderr)
        sys.exit(1)
    client = SilimindMCPClient(url, token)
    if len(sys.argv) > 1 and sys.argv[1] != "list":
        name = sys.argv[1]
        kwargs = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        result = call_tool(client, name, kwargs)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        tools = get_tools(client)
        for t in tools:
            print(f"  {t['name']:30s} {t.get('description', '')[:70]}")


if __name__ == "__main__":
    main()
