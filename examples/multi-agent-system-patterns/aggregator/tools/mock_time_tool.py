"""Mock time tool for multi-agent system patterns.

This module provides a mock time tool that returns the current time
for demonstration purposes in the multi-agent system patterns examples.
"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class MockTimeToolInput(BaseModel):
    """Input for the mock time tool."""

    timezone: str = Field(default="UTC", description="Timezone for the time (e.g., UTC, EST, PST)")


class MockTimeTool(BaseTool):
    """Gets the current time (mocked for demo purposes)."""

    name: str = "mock_time"
    description: str = "Gets the current time (mocked for demo purposes)."
    args_schema: type[BaseModel] = MockTimeToolInput

    def _run(self, timezone: str = "UTC", **_kwargs: Any) -> str:
        _ = timezone
        return "Current time: 03:00 AM UTC"
