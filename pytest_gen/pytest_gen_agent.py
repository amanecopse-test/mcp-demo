import asyncio
import textwrap

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel

base_url = "https://my-kaggle-ollama-app.serveo.net"
model = ChatOllama(model="mistral-small", base_url=base_url)
server_params = StdioServerParameters(
    command="python",
    args=["pytest_gen_server.py"],
)


class Response(BaseModel):
    test_code: str


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)

            agent = create_react_agent(model, tools, response_format=Response, prompt="")
            agent_response = await agent.ainvoke({"messages": [
                SystemMessage(textwrap.dedent(
                    """
                    Write and verify the pytest unit test of Python source code according to the instructions below.
                    1. Gets the Python source code for the specified path.
                    2. Create a pytest test code and write it as a py file in the same path as the source code (in the format xxx_test.py).
                    3. Check coverage on the same folder path.
                    4. Repeat 1 to 3 until coverage is True, and if True, respond test_code.
                    """
                )),
                HumanMessage(textwrap.dedent(
                    """
                    Source code path: ./mock_project/calculator.py
                    """
                )),
            ]})
            for e in agent_response['messages']:
                if hasattr(e, 'content'):
                    print(e.content)
                if hasattr(e, 'tool_calls'):
                    print(e.tool_calls)


if __name__ == "__main__":
    asyncio.run(run())
