from mcp.server import MCPServer
import sqlite3

mcp = MCPServer("Simple Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@mcp.resource("calculator://help")
def calculator_help() -> str:
    """Provide information about the calculator."""
    return """
    Calculator Help:

    add(a, b)       - Add two numbers.
    subtract(a, b)  - Subtract b from a.
    multiply(a, b)  - Multiply two numbers.
    divide(a, b)    - Divide a by b.
    """

@mcp.resource("calculator://calculations")
def calculator_calculations() -> str:
    """Provide stored calculations from the database."""
    
    connection = sqlite3.connect("calculator.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, expression, result FROM calculations ORDER BY id"
    )

    rows = cursor.fetchall()
    connection.close()

    if not rows:
        return "No calculations found."

    return "\n".join(
        f"{row[0]}. {row[1]} = {row[2]}"
        for row in rows
    )
    
@mcp.prompt()
def calculator_explanation(expression: str) -> str:
    """Create a prompt for explaining a calculation."""
    return f"Explain the calculation '{expression}' clearly and step by step."

if __name__ == "__main__":
    mcp.run()