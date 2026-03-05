"""Mock get_expenses tool with intentionally large raw output."""

from __future__ import annotations

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class GetExpensesInput(BaseModel):
    """Input schema for get_expenses."""

    user_id: int = Field(description="Team member user ID")
    quarter: str = Field(description="Fiscal quarter, for example Q3")


class GetExpensesTool(BaseTool):
    """Return quarterly expense line items by user."""

    name: str = "get_expenses"
    description: str = "Get expense line items for a user and quarter"
    args_schema: type[BaseModel] = GetExpensesInput

    def _run(self, user_id: int, quarter: str) -> dict[str, Any]:
        if quarter.strip().upper() != "Q3":
            return {
                "status": "not_found",
                "message": f"No expense data found for quarter '{quarter}'.",
                "data": {"user_id": user_id, "quarter": quarter, "items": []},
            }

        categories = ["flight", "hotel", "meal", "ground_transport", "conference_fee"]
        items = []

        for i in range(1, 37):
            base = 70 + ((user_id * 19 + i * 23) % 260)
            if user_id % 5 == 0:
                base += 120
            elif user_id % 3 == 0:
                base += 60

            amount = float(f"{base + (i % 7) * 0.49:.2f}")
            category = categories[(user_id + i) % len(categories)]

            items.append(
                {
                    "expense_id": f"EXP-{user_id}-{i:03d}",
                    "date": f"2026-0{((i - 1) % 3) + 7}-{((i * 3) % 28) + 1:02d}",
                    "category": category,
                    "amount": amount,
                    "currency": "USD",
                    "merchant": f"{category}-vendor-{(i % 9) + 1}",
                    "receipt_note": (
                        "Corporate travel expense with attached receipt metadata, policy tag, "
                        "project code, approver trail, and reconciliation markers for audit processing."
                    ),
                }
            )

        return {
            "status": "ok",
            "message": f"Found {len(items)} expense line items for user_id {user_id} in Q3.",
            "data": {"user_id": user_id, "quarter": "Q3", "items": items},
        }
