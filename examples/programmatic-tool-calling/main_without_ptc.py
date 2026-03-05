"""Scenario demo without Programmatic Tool Calling (PTC)."""

from dotenv import load_dotenv

from glaip_sdk.agents import Agent
from tools import GetBudgetByLevelTool, GetExpensesTool, GetTeamMembersTool

load_dotenv(override=True)

query = "Which Engineering team members exceeded their Q3 travel budget?"

agent = Agent(
    name="budget_audit_without_ptc",
    model="openai/gpt-5.2",
    instruction=(
        "You are a finance audit assistant with tool access. "
        'For this toolset: team members are in get_team_members(...)["data"]["members"], '
        'budgets are in get_budget_by_level(...)["data"]["quarterly_budget"], '
        'and expense items are in get_expenses(...)["data"]["items"]. '
        "Each returned expense item is already part of the Q3 travel-expense dataset, so sum all item.amount values (do not filter by category). "
        "Audit every Engineering member before answering: for each member get expenses and budget, compute total, then compare total > budget. "
        "Do not claim nobody exceeded budget unless all members were evaluated and the exceeded list is empty. "
        "Use tools when needed, validate tool responses before reading nested fields, "
        "handle not_found/error statuses safely, and avoid guessing. "
        "Perform calculations from tool data and return concise final results with exceeded count and names."
    ),
    tools=[GetTeamMembersTool(), GetExpensesTool(), GetBudgetByLevelTool()],
)

agent.run(query, local=True, verbose=True)
