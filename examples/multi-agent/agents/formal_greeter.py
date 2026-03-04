"""Formal Greeter - sub-agent for formal greetings."""

from glaip_sdk.agents import Agent
from tools import greeting_tool, time_tool

INSTRUCTION = """You are a formal greeting specialist.

When asked to greet someone:
1. Use the greeting tool with style='formal'
2. Maintain a professional and dignified tone
3. Be polite and respectful
4. Use the time tool when users inquire about the current time
"""

formal_greeter = Agent(
    name="formal_greeter",
    instruction=INSTRUCTION,
    description="Provides formal, professional greetings",
    tools=[greeting_tool, time_tool],
)

__all__ = ["formal_greeter"]
