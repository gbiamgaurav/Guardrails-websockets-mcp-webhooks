
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import asyncio


from langchain.agents import create_agent

import os 
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command":"python",
                "args":["mathserver.py"], # ensure correct absolute path
                "transport":"stdio",
                },

            "weather": {
                "url":"http://localhost:8000/mcp", # ensure server is running here
                "transport": "streamable_http",
            }

        }
    )

    tools = await client.get_tools()
    model = ChatGroq(model="qwen/qwen3-32b")

    agent = create_agent(
        model, tools
    )

    # math_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "what's (3 +5) * 12?"}]}
    # )
    
    
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in Jaipur?"}]}
    )



    # print("Math response:", math_response['messages'][-1].content)
    
    print("Weather response:", weather_response['messages'][-1].content)

asyncio.run(main())