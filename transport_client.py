import asyncio
import os
import traceback
import httpx2
from mcp.client.streamable_http import streamable_http_client
from mcp import Client
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

transport = os.getenv("MCP_TRANSPORT", "stdio")
host = os.getenv("MCP_HOST", "127.0.0.1")
port = int(os.getenv("MCP_PORT", "8000"))
server_url = f"http://{host}:{port}/mcp"
token = os.getenv("MCP_AUTH_TOKEN", "mcp-secret-123")

async def test_client(client):
    tools = await client.list_tools()
    print("\nTools:")
    for tool in tools.tools:
        print("-", tool.name)
    result = await client.call_tool("add", {"a": 10, "b": 20})
    print("\nAdd Result:")
    print(result.structured_content)

    resource = await client.read_resource("calculator://help")
    print("\nResource:")
    print(resource)

    prompt = await client.get_prompt(
        "explain_calculation",
        arguments={"expression": "10 + 20"}
    )
    print("\nPrompt:")
    print(prompt)

async def run_stdio():
    server_params = StdioServerParameters(
        command="python",
        args=["transport_server.py"],
        env={**os.environ, "MCP_TRANSPORT": "stdio"}
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as client:
                await client.initialize()
                print("\nConnected using STDIO")
                await test_client(client)

    except Exception:
        print("\nSTDIO ERROR:")
        traceback.print_exc()

async def run_http():
    print(f"\nConnecting to {server_url}")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        async with httpx2.AsyncClient(
            headers=headers
        ) as http_client:

            async with streamable_http_client(
                server_url,
                http_client=http_client
            ) as (read, write):

                async with ClientSession(
                    read,
                    write
                ) as client:

                    await client.initialize()

                    print(
                        "Connected using "
                        "Authenticated Streamable HTTP"
                    )
                    await test_client(client)
    except Exception:
        print("\nHTTP ERROR:")
        traceback.print_exc()

async def main():
    print("================================")
    print("       MCP")
    print("================================")
    print("Transport:", transport)
    print("Server:", server_url)

    if transport == "streamable-http":
        await run_http()
    else:
        await run_stdio()

if __name__ == "__main__":
    asyncio.run(main())