"""Employee lookup tool and agent fixture for evaluation examples."""

from __future__ import annotations

from glaip_sdk.agents import Agent
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

_EMPLOYEES: dict[str, list[str]] = {
    "Engineering": ["Alice Chen", "Bob Smith", "Carol Wu"],
    "Marketing": ["David Lee", "Eve Johnson"],
    "Finance": ["Frank Brown", "Grace Kim", "Henry Park"],
}


class EmployeeLookupInput(BaseModel):
    """Input schema for the employee lookup tool."""

    department: str = Field(description="Department name to look up employees for")


class EmployeeLookupTool(BaseTool):
    """Look up employees by department."""

    name: str = "employee_lookup"
    description: str = (
        "Look up employees in a given department. Returns a list of employee names."
    )
    args_schema: type[BaseModel] = EmployeeLookupInput

    def _run(self, department: str, **_kwargs: object) -> str:
        """Return the employees in the requested department."""
        employees = _EMPLOYEES.get(department, [])
        return (
            ", ".join(employees) if employees else f"No employees found in {department}"
        )


def build_employee_lookup_agent() -> Agent:
    """Build the agent used by the local and hosted evaluation examples."""
    return Agent(
        name="employee-lookup-example-agent",
        instruction=(
            "You are an HR assistant. Use the employee_lookup tool to look up employees by "
            "department whenever a user asks who works in a department. Do not answer from memory."
        ),
        description="Example agent that answers HR questions via the employee lookup tool.",
        filesystem=False,
        tools=[EmployeeLookupTool],
    )


__all__ = ["EmployeeLookupTool", "build_employee_lookup_agent"]
