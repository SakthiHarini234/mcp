import asyncio
from mcp import Client
from server import mcp

async def main():

    print("Starting MCP Client...")

    async with Client(mcp) as client:

        print("MCP Client connected to Server.")

        # 1. Capability Negotiation
        capabilities = client.server_capabilities

        print("\nServer Capabilities:")
        print(capabilities)

        # 2. List Tools
        result = await client.list_tools()

        print("\nAvailable Tools:")

        for tool in result.tools:
            print(f"- {tool.name}")

        # 3. Progress Notification
        print("\nSending progress notifications...")

        await client.send_progress_notification(
            progress_token="calculator-task",
            progress=25,
            total=100
        )

        print("Progress: 25%")

        await client.send_progress_notification(
            progress_token="calculator-task",
            progress=50,
            total=100
        )

        print("Progress: 50%")

        await client.send_progress_notification(
            progress_token="calculator-task",
            progress=75,
            total=100
        )

        print("Progress: 75%")

        await client.send_progress_notification(
            progress_token="calculator-task",
            progress=100,
            total=100
        )

        print("Progress: 100%")

        print("Progress notifications completed.")

        # 4. Pagination
        print("\nPagination Example:")

        tools = result.tools
        page_size = 2

        for page_number, start in enumerate(
            range(0, len(tools), page_size),
            start=1
        ):
            page = tools[start:start + page_size]

            print(f"\nPage {page_number}:")

            for tool in page:
                print(f"- {tool.name}")

        # 5. Cancellation
        print("\nCancellation Example:")

        async def long_running_task():

            for i in range(1, 11):

                print(f"Task progress: {i}/10")

                await asyncio.sleep(1)

            return "Task completed."

        task = asyncio.create_task(long_running_task())

        # Allow the task to run for a short time.
        await asyncio.sleep(3)

        print("\nCancelling the task...")

        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            print("Task cancelled successfully.")

        # 6. Progress
        print("\nProgress Example:")

        total_steps = 5

        for step in range(1, total_steps + 1):

            progress = (step / total_steps) * 100

            print(
                f"Progress: {progress:.0f}% "
                f"(Step {step}/{total_steps})"
            )

            await asyncio.sleep(0.5)

        print("Progress tracking completed.")

        # 7. Logging
        print("\nLogging Example:")
                # 7.8 Logging
        print("\nLogging Example:")

        print("MCP Logging capability is deprecated in the current SDK.")
        print("The SDK reports this through MCPDeprecationWarning.")
        print("Logging should now be handled using the application's logging system.")

        import logging

        logging.basicConfig(level=logging.INFO)

        logger = logging.getLogger("mcp-learning")

        logger.info("MCP client started.")
        logger.info("Calculator tools are available.")
        logger.warning("This is a sample warning.")
        print("Logging helps monitor MCP client/server activity.")

if __name__ == "__main__":
    asyncio.run(main())