"""Hello World Single Agent - Tools module."""

from tools.greeting import GreetingTool
from glaip_sdk.tools import Tool

time_tool = Tool.from_native("time_tool")

__all__ = ["GreetingTool", time_tool]
