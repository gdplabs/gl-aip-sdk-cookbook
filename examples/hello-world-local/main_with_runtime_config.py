"""Hello World - Single Agent Example with Runtime Configuration."""

import os
from typing import Any

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
        authentication={"type": "custom-header", "headers": {"x-api-key": "example", "Authorization": "Bearer example"}},
    )

research_agent = Agent(
    name="research_agent",
    instruction="You are a research assistant that helps find and format academic papers.",
    tools=[ResearchFormatterTool],
    mcps=[arxiv_mcp] if arxiv_mcp else [],
)

runtime_config: dict[str, Any] = {
    "agent_config": {"planning": True},
    "tool_configs": {ResearchFormatterTool: {"style": "brief", "max_results": 3}},
}

if arxiv_mcp:
    runtime_config["mcp_configs"] = {arxiv_mcp: {"authentication": {"type": "custom-header", "headers": {"x-api-key": _api_key, "Authorization": f"Bearer {_auth_token}"}}}}

research_agent.run("Hello! Can you help me find papers about transformers?", runtime_config=runtime_config)
