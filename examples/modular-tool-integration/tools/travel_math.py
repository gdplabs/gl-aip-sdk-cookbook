"""Travel budget calculator tool for the travel assistant example.

Demonstrates a simple, single-file tool implementation.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class TravelMathInput(BaseModel):
    """Input schema for the travel math tool."""

    expression: str = Field(description="The arithmetic expression to evaluate")


class TravelMathTool(BaseTool):
    """Tool for performing travel-related calculations."""

    name: str = "travel_calculator"
    description: str = "Performs currency conversion and travel budget calculations."
    args_schema: type[BaseModel] = TravelMathInput

    def _run(self, expression: str, **kwargs: Any) -> str:
        """Perform calculation logic.

        Args:
            expression: The arithmetic expression to evaluate.
            **kwargs: Additional execution arguments.

        Returns:
            Calculation result string.
        """
        return f"Calculation result for '{expression}': 1250.00"
