import asyncio
import json
import os
from dotenv import load_dotenv
from groq import Groq
from mcp import Client
from server import mcp

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def main():
    # Connect to MCP server
    async with Client(mcp) as mcp_client:
        tool_result = await mcp_client.list_tools()
        groq_tools = []

        for tool in tool_result.tools:
            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.input_schema
                }
            })
        print("MCP tools connected to Groq:")
        for tool in groq_tools:
            print("-", tool["function"]["name"])
        # User question
        user_input = input("\nAsk something: ")

        messages = [
            {
                "role": "user",
                "content": user_input
            }
        ]

        #Groq decide whether to use a tool
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=groq_tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # Check whether Groq requested a tool
        if assistant_message.tool_calls:
            messages.append(
                assistant_message.model_dump(exclude_none=True)
            )

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print(f"\nGroq selected MCP tool: {tool_name}")
                print(f"Arguments: {arguments}")

                #Execute MCP tool
                tool_result = await mcp_client.call_tool(
                    tool_name,
                    arguments
                )

                print("MCP result:", tool_result.structured_content)
                #MCP result to Groq
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        tool_result.structured_content
                    )
                })
            #Groq generates final answer
            final_response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages
            )
            print("\nFinal answer:")
            print(final_response.choices[0].message.content)
        else:
            #Groq answer without MCP tool
            print("\nAnswer:")
            print(assistant_message.content)

if __name__ == "__main__":
    asyncio.run(main())