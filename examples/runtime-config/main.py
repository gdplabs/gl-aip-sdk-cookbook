"""Hello World - Single Agent Example with Runtime Configuration."""

from glaip_sdk import Agent

from mcps import arxiv_mcp
from tools import ResearchFormatterTool

research_agent = Agent(
    name="research_agent",
    instruction="You are a research assistant that helps users find and summarize academic papers.",
    description="Research assistant with configurable formatting",
    tools=[ResearchFormatterTool],
    mcps=[arxiv_mcp] if arxiv_mcp else [],
)
research_agent.deploy()
research_agent.run(
    "Find papers about transformers.",
    runtime_config={
        "agent_config": {"planning": True},
        "tool_configs": {ResearchFormatterTool: {"style": "brief", "max_results": 3}},
        "mcp_configs": {arxiv_mcp: {"authentication": {"type": "custom-header"}}},
    },
)
