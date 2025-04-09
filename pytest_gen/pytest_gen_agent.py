import asyncio
import optparse
import textwrap

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel

opt_parser = optparse.OptionParser()
opt_parser.add_option("--ollama", action="store_true", default=False, dest="ollama")
opt_parser.add_option("--ollama-url", default="https://my-kaggle-ollama-app.serveo.net", dest="ollama_url")
opt_parser.add_option("--ollama-model", default="mistral-small", dest="ollama_model")
opt_parser.add_option("--gemini", action="store_true", default=False, dest="gemini")
opt_parser.add_option("--gemini-key", default=None, dest="gemini_key")
opt_parser.add_option("--gemini-model", default="gemini-2.0-flash", dest="gemini_model")
opt_parser.add_option("--source-path", default="./pytest_gen/mock_project/calculator.py", dest="source_path")
options, args = opt_parser.parse_args()

if options.ollama:
    model = ChatOllama(model="mistral-small", base_url=options.ollama_url)
if options.gemini:
    model = ChatGoogleGenerativeAI(model=options.gemini_model, api_key=options.gemini_key)

server_params = StdioServerParameters(
    command="python",
    args=["pytest_gen/pytest_gen_server.py"],
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
                    f"""
                    Use tools: {tools}
                    Write and verify the pytest unit test of Python source code according to the instructions below.
                    1. Gets the Python source code for the specified path.
                    2. Create a pytest test code and write it as a py file in the same path as the source code (in the format xxx_test.py).
                    3. Check coverage on the same folder path.
                    4. Repeat 1 to 3 until coverage is True, and if True, respond test_code.
                    """
                )),
                HumanMessage(textwrap.dedent(
                    f"""
                    Source code path: {options.source_path}
                    """
                )),
            ]})
            for e in agent_response['messages']:
                if hasattr(e, 'content'):
                    print(e.content)
                if hasattr(e, 'tool_calls'):
                    print(e.tool_calls)
            print("-------------------------Result-------------------------")
            print(agent_response["structured_response"].test_code)


if __name__ == "__main__":
    asyncio.run(run())
