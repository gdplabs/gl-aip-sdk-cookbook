"""Flight status tool for the travel assistant example.

Demonstrates a simple, single-file tool implementation.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class FlightStatusInput(BaseModel):
    """Input schema for the flight status tool."""

    flight_number: str = Field(description="The flight number to check (e.g., GA123)")


class FlightStatusTool(BaseTool):
    """Tool for checking the status of a flight."""

    name: str = "get_flight_status"
    description: str = "Returns the status of a flight by flight number."
    args_schema: type[BaseModel] = FlightStatusInput

    def _run(self, flight_number: str, **kwargs: Any) -> str:
        """Run the flight status check.

        Args:
            flight_number: The flight number to check (e.g., GA123).
            **kwargs: Additional execution arguments.

        Returns:
            Current status of the flight.
        """
        return f"Flight {flight_number} is currently on time."
