"""Mock weather tool for multi-agent system patterns.

This module provides a mock weather tool that returns weather forecasts
for demonstration purposes in the multi-agent system patterns examples.
"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class MockWeatherToolInput(BaseModel):
    """Input for the mock weather tool."""

    location: str = Field(
        default="current",
        description="Location for weather forecast (e.g., current, city name)",
    )


class MockWeatherTool(BaseTool):
    """Gets weather forecast for a location (mocked for demo purposes)."""

    name: str = "mock_weather"
    description: str = "Gets weather forecast for a location (mocked for demo purposes)."
    args_schema: type[BaseModel] = MockWeatherToolInput

    def _run(self, location: str = "current", **_kwargs: Any) -> str:
        _ = location
        return """Today's weather: Partly cloudy with rain expected at 3 PM, temperature 72°F"""
