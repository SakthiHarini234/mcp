import asyncio
import json
from groq import Groq
from dotenv import load_dotenv
from mcp import Client
from server import mcp

load_dotenv()

groq_client = Groq()

MODEL = "openai/gpt-oss-120b"

async def main():

    async with Client(mcp) as mcp_client:

        # 1. Get available MCP tools

        result = await mcp_client.list_tools()

        print("Available MCP Tools:")

        for tool in result.tools:
            print(f"- {tool.name}")

        # 2. Convert MCP tools to Groq tool format

        groq_tools = []

        for tool in result.tools:

            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.input_schema
                }
            })

        # 3. Get user input

        user_input = input("\nEnter your question: ")

        messages = [
            {
                "role": "user",
                "content": user_input
            }
        ]

        # 4. Agent Loop

        while True:

            print("\nCalling LLM...")

            response = groq_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=groq_tools,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message
            messages.append(assistant_message)

            # 5. Check whether LLM wants to call a tool

            if not assistant_message.tool_calls:

                print("\nFinal Answer:")
                print(assistant_message.content)

                break

            # 6. Execute requested MCP tools
            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print(
                    f"\nCalling MCP Tool: "
                    f"{tool_name}({arguments})"
                )
                # Human Approval
                approval_required = tool_name == "divide"

                if approval_required:

                    print(
                        f"\nHuman approval required for: "
                        f"{tool_name}"
                    )

                    approval = input(
                        "Do you want to execute this tool? (y/n): "
                    )

                    if approval.lower() != "y":

                        print("\nTool execution cancelled by user.")

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": "Tool execution was rejected by the user."
                        })

                        continue

                # Execute MCP tool

                try:

                    tool_result = await mcp_client.call_tool(
                        tool_name,
                        arguments=arguments
                    )

                    if tool_result.is_error:

                        tool_content = f"Tool error: {tool_result}"

                        print("\nTool Error:")
                        print(tool_content)

                    else:

                        tool_content = str(tool_result)

                        print("\nTool Result:")
                        print(tool_content)

                except Exception as error:

                    tool_content = (
                        f"Tool execution failed: {error}"
                    )

                    print("\nTool Execution Error:")
                    print(tool_content)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_content
                })

            # 8. Loop continues

            print("\nTool result sent back to LLM.")

            # The LLM can now decides to call another tool or give the final answer.

if __name__ == "__main__":
    asyncio.run(main())