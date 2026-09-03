import asyncio

from mcp import Client
from server import mcp


async def main():
    async with Client(mcp) as client:

        result = await client.list_tools()

        print("Available tools:")

        for tool in result.tools:
            print(f"- {tool.name}")

        print("\nTool Details:")

        for tool in result.tools:
            print("\nTool:", tool.name)
            print("Description:", tool.description)
            print("Schema:", tool.input_schema)


if __name__ == "__main__":
    asyncio.run(main())