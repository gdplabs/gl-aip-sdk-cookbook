"""Scenario demo with Programmatic Tool Calling (PTC)."""

from dotenv import load_dotenv

from glaip_sdk.agents import Agent
from glaip_sdk.ptc import PTC
from tools import GetBudgetByLevelTool, GetExpensesTool, GetTeamMembersTool

load_dotenv(override=True)

query = "Which Engineering team members exceeded their Q3 travel budget?"

agent = Agent(
    name="budget_audit_with_ptc",
    model="openai/gpt-5.2",
    instruction=(
        "You are a finance audit assistant with tools and execute_ptc_code available. "
        "For tasks that need tools, prefer execute_ptc_code so orchestration happens in code instead of repeated model turns. "
        'For this toolset: team members are in get_team_members(...)["data"]["members"], '
        'budgets are in get_budget_by_level(...)["data"]["quarterly_budget"], '
        'and expense items are in get_expenses(...)["data"]["items"]. '
        "Each returned expense item is already part of the Q3 travel-expense dataset, so sum all item.amount values (do not filter by category). "
        "In code, use loops/conditionals/aggregation as needed, validate tool responses before reading nested fields, "
        "handle not_found/error statuses safely, and return only concise final results. "
        "If a request does not need tools, answer directly."
    ),
    tools=[GetTeamMembersTool(), GetExpensesTool(), GetBudgetByLevelTool()],
    ptc=PTC(enabled=True, sandbox_timeout=180.0),
)

agent.run(query, local=True, verbose=True)
