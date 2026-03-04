"""Mock calendar tool for multi-agent system patterns.

This module provides a mock calendar tool that returns calendar events
for demonstration purposes in the multi-agent system patterns examples.
"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class MockCalendarToolInput(BaseModel):
    """Input for the mock calendar tool."""

    date: str = Field(
        default="today",
        description="Date to get calendar events for (e.g., today, tomorrow)",
    )


class MockCalendarTool(BaseTool):
    """Gets calendar events for a given date (mocked for demo purposes)."""

    name: str = "mock_calendar"
    description: str = "Gets calendar events for a given date (mocked for demo purposes)."
    args_schema: type[BaseModel] = MockCalendarToolInput

    def _run(self, date: str = "today", **_kwargs: Any) -> str:
        _ = date
        return """Today's main calendar highlight: Meeting at 2 PM with the development team"""
