
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """_summary_

    Args:
        location (str): _description_

    Returns:
        str: _description_
    """
    return "It's always raining in California"


# Streamable-http runs on server

if __name__ == "__main__":
    mcp.run(transport="streamable-http")