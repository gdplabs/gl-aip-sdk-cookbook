"""PTC baseline: use MCP tools with code execution."""

from dotenv import load_dotenv

from glaip_sdk.agents import Agent
from glaip_sdk.mcps import MCP
from glaip_sdk.ptc import PTC

load_dotenv(override=True)

deepwiki_mcp = MCP(
    name="deepwiki",
    transport="http",
    description="DeepWiki MCP for accessing public GitHub repository documentation",
    config={"url": "https://mcp.deepwiki.com/mcp"},
)

agent = Agent(
    name="ptc_with_mcp_example",
    model="openai/gpt-5.2",
    instruction="You are a helpful assistant with access to deepwiki and sandbox Python.",
    mcps=[deepwiki_mcp],
    ptc=PTC(enabled=True),
)

agent.run("Calculate how many words are in wiki structure of 'anthropics/claude-code' via code", local=True)
