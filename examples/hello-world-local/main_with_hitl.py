"""Hello World - Single Agent Example with Human-in-the-Loop (HITL)."""

from glaip_sdk.agents import Agent
from tools import SimpleGreetingTool

hello_agent = Agent(
    name="hello_local_agent",
    instruction="You are a friendly greeting assistant.",
    tools=[SimpleGreetingTool],
    tool_configs={SimpleGreetingTool: {"hitl": {"timeout_seconds": 10}}},
    agent_config={"hitl_enabled": True},
)

hello_agent.run("Please give me an enthusiastic greeting! My name is Christian.")
