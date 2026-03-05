"""Mock get_team_members tool."""

from __future__ import annotations

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class GetTeamMembersInput(BaseModel):
    """Input schema for get_team_members."""

    department: str = Field(description="Department name, for example Engineering")


class GetTeamMembersTool(BaseTool):
    """Return team members for a department."""

    name: str = "get_team_members"
    description: str = "Get team members with id, name, and level for a department"
    args_schema: type[BaseModel] = GetTeamMembersInput

    def _run(self, department: str) -> dict[str, Any]:
        if department.strip().lower() != "engineering":
            return {
                "status": "not_found",
                "message": f"No team found for department '{department}'.",
                "data": {"members": []},
            }

        members = [
            {"id": 101, "name": "Ava", "level": "L3"},
            {"id": 102, "name": "Noah", "level": "L4"},
            {"id": 103, "name": "Mia", "level": "L3"},
            {"id": 104, "name": "Ethan", "level": "L5"},
            {"id": 105, "name": "Sophia", "level": "L4"},
            {"id": 106, "name": "Liam", "level": "L3"},
            {"id": 107, "name": "Olivia", "level": "L5"},
            {"id": 108, "name": "Lucas", "level": "L4"},
            {"id": 109, "name": "Emma", "level": "L3"},
            {"id": 110, "name": "James", "level": "L5"},
            {"id": 111, "name": "Amelia", "level": "L4"},
            {"id": 112, "name": "Benjamin", "level": "L3"},
        ]

        return {
            "status": "ok",
            "message": f"Found {len(members)} team members for Engineering.",
            "data": {"members": members},
        }
