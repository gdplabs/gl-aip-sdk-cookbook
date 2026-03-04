"""Hello World Multi-Agent - Tools module.

Exports:
    FarewellTool, GreetingTool: Tool classes for direct use
    farewell_tool, greeting_tool, time_tool: Shared tool instances
"""

from glaip_sdk.tools import Tool
from tools.farewell import FarewellTool
from tools.greeting import GreetingTool

# Shared tool instances - import these in agents for reuse
time_tool = Tool.from_native("time_tool")
greeting_tool = GreetingTool
farewell_tool = FarewellTool

__all__ = [
    "FarewellTool",
    "GreetingTool",
    "farewell_tool",
    "greeting_tool",
    "time_tool",
]
