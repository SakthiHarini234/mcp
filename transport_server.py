import os
from mcp.server import MCPServer
from pydantic import AnyHttpUrl
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings

AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN", "mcp-secret-123")

host = os.getenv("MCP_HOST", "127.0.0.1")
port = int(os.getenv("MCP_PORT", "8001"))

class SimpleTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        if token == AUTH_TOKEN:
            return AccessToken(token=token, client_id="phase8-client", scopes=["calculator"],)
        return None

mcp = MCPServer(
    "Phase 8 Server",
    token_verifier=SimpleTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("https://example.com"),
        resource_server_url=AnyHttpUrl(
            f"http://{host}:{port}/mcp"
        ),
        required_scopes=["calculator"],
    ),
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@mcp.tool()
def server_info() -> str:
    """Return server information."""
    return "MCP Phase 8 Server"

@mcp.resource("calculator://help")
def help_resource() -> str:
    """Calculator help."""
    return "Available tools: add, divide, server_info"

@mcp.prompt()
def explain_calculation(expression: str) -> str:
    """Create a calculation explanation prompt."""
    return f"Explain this calculation step by step: {expression}"

transport = os.getenv("MCP_TRANSPORT", "stdio")
host = os.getenv("MCP_HOST", "127.0.0.1")
port = int(os.getenv("MCP_PORT", "8000"))

if __name__ == "__main__":
    if transport == "streamable-http":
        print(f"HTTP MCP Server: http://{host}:{port}/mcp", file=__import__("sys").stderr)
        mcp.run(transport="streamable-http", host=host, port=port)

    else:
        mcp.run()