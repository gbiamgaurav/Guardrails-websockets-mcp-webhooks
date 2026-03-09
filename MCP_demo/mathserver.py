
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int, b: int) -> int:
    """_summary_

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    return a + b 

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """_summary_

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    return a * b


# The transport="stdio" argument tells the server to:
# use standard input/output (stdin and stdout) to receive and respond to tool function calls.
# Local servers


if __name__ == "__main__":
    mcp.run(transport="stdio")