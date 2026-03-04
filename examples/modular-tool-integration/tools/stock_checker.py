"""Stock checker tool for the travel assistant example.

Demonstrates a simple, single-file tool implementation.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class StockCheckerInput(BaseModel):
    """Input schema for the stock checker tool."""

    ticker: str = Field(description="The stock ticker symbol (e.g., AAPL)")


class StockCheckerTool(BaseTool):
    """Tool for checking airline stock prices."""

    name: str = "get_stock_price"
    description: str = "Returns the current stock price for a given ticker symbol."
    args_schema: type[BaseModel] = StockCheckerInput

    def _run(self, ticker: str, **kwargs: Any) -> str:
        """Run the stock price check.

        Args:
            ticker: The stock ticker symbol (e.g., AAPL).
            **kwargs: Additional execution arguments.

        Returns:
            Current stock price string.
        """
        return f"The stock price for {ticker} is $150.25."
