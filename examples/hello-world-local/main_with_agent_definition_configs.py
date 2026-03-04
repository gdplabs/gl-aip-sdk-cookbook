"""Hello World - Single Agent Example with Agent Definition Configurations."""

import os

from glaip_sdk.agents import Agent
from glaip_sdk.mcps import MCP
from tools import ResearchFormatterTool

_api_key = os.getenv("ARXIV_MCP_API_KEY")
_auth_token = os.getenv("ARXIV_MCP_AUTH_TOKEN")

arxiv_mcp: MCP | None = None
if _api_key and _auth_token:
    arxiv_mcp = MCP(
        name="arxiv-mcp",
        transport="http",
        config={"url": "https://api.bosa.id/arxiv/mcp/"},
        authentication={"type": "custom-header", "headers": {"x-api-key": "placeholder", "Authorization": "Bearer placeholder"}},
    )

research_agent = Agent(
    name="research_agent_with_configs",
    instruction="You are a research assistant that helps find and format academic papers.",
    tools=[ResearchFormatterTool],
    mcps=[arxiv_mcp] if arxiv_mcp else [],
    agent_config={"planning": False},
    tool_configs={ResearchFormatterTool: {"style": "detailed", "max_results": 10, "include_links": True}},
    mcp_configs={arxiv_mcp: {"authentication": {"type": "custom-header", "headers": {"x-api-key": _api_key, "Authorization": f"Bearer {_auth_token}"}}}} if arxiv_mcp else {},
)

research_agent.run("Format some research about machine learning transformers.")
