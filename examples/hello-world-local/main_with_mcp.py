"""Hello World - Single Agent Example with MCP Integration."""

from glaip_sdk.agents import Agent
from tools import SimpleGreetingTool
from mcps import arxiv_mcp, deepwiki_mcp

mcps = [mcp for mcp in [arxiv_mcp, deepwiki_mcp] if mcp is not None]
hello_agent = Agent(
    name="hello_local_agent_mcp",
    instruction="You are a friendly assistant with access to MCP servers.",
    tools=[SimpleGreetingTool],
    mcps=mcps,
)

hello_agent.run("Search for information about Python async programming.")
