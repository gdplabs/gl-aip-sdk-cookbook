"""Mock get_budget_by_level tool."""

from __future__ import annotations

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class GetBudgetByLevelInput(BaseModel):
    """Input schema for get_budget_by_level."""

    level: str = Field(description="Employee level, for example L3")


class GetBudgetByLevelTool(BaseTool):
    """Return travel budget by employee level."""

    name: str = "get_budget_by_level"
    description: str = "Get quarterly travel budget limit by employee level"
    args_schema: type[BaseModel] = GetBudgetByLevelInput

    def _run(self, level: str) -> dict[str, Any]:
        budgets = {
            "L3": 5000.0,
            "L4": 7000.0,
            "L5": 9500.0,
        }

        normalized_level = level.strip().upper()
        if normalized_level not in budgets:
            return {
                "status": "not_found",
                "message": f"No budget configured for level '{level}'.",
                "data": None,
            }

        return {
            "status": "ok",
            "message": f"Budget found for level {normalized_level}.",
            "data": {"level": normalized_level, "quarterly_budget": budgets[normalized_level]},
        }
