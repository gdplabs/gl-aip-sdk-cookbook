"""Weather tool package for the modular tool integration example.

This package demonstrates how to organize a tool with helper files.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from .service import get_mock_weather


class WeatherInput(BaseModel):
    """Input schema for the weather tool."""

    city: str = Field(description="The city to check weather for")


class WeatherTool(BaseTool):
    """Tool for getting current weather information.

    This tool demonstrates modular tool development by using a helper service.
    """

    name: str = "get_weather"
    description: str = "Returns current weather for a city."
    args_schema: type[BaseModel] = WeatherInput

    def _run(self, city: str, **kwargs: Any) -> str:
        """Run the weather tool logic.

        Args:
            city: The city to check weather for.
            **kwargs: Additional execution arguments.

        Returns:
            Current weather forecast string.
        """
        return get_mock_weather(city)
