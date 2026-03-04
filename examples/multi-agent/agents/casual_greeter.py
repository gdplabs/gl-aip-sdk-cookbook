"""Casual Greeter - sub-agent for casual greetings."""

from glaip_sdk.agents import Agent
from tools import farewell_tool, greeting_tool, time_tool

INSTRUCTION = """You are a casual greeting specialist.

When asked to greet someone:
1. Use the greeting tool with style='casual' or 'enthusiastic'
2. Be friendly and relaxed
3. You can also say goodbye using the farewell tool
4. Use the time tool when users ask about time
"""

# NOTE: Tool instances are imported from tools module - shared across all agents
casual_greeter = Agent(
    name="casual_greeter",
    instruction=INSTRUCTION,
    description="Provides casual, friendly greetings and farewells",
    tools=[greeting_tool, farewell_tool, time_tool],
)

__all__ = ["casual_greeter"]
