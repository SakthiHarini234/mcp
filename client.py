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

        resources = await client.list_resources()
        print("\nResources:")
        for resource in resources.resources:
            print(resource)

        resource_content = await client.read_resource("calculator://help")
        print("\nResource Content:")
        print(resource_content)

        prompts = await client.list_prompts()
        print("\nPrompts:")
        for prompt in prompts.prompts:
            print(prompt)

        prompt_result = await client.get_prompt("calculator_explanation", arguments={"expression": "10 + 20"})
        print("\nPrompt Result:")
        print(prompt_result)

        database_content = await client.read_resource("calculator://calculations")
        print("\nDatabase Calculations:")
        print(database_content)

if __name__ == "__main__":
    asyncio.run(main())