"""Simple comparison for large-output budget audit scenario."""

from time import perf_counter

from dotenv import load_dotenv

from glaip_sdk.agents import Agent
from glaip_sdk.ptc import PTC
from tools import GetBudgetByLevelTool, GetExpensesTool, GetTeamMembersTool

load_dotenv(override=True)

QUERY = "Which Engineering team members exceeded their Q3 travel budget?"
RUNS = 1
SHOW_RESPONSES = False

without_duration = []
without_wall = []
without_tokens = []
without_llm_steps = []

with_duration = []
with_wall = []
with_tokens = []
with_llm_steps = []

print("\n=== WITHOUT PTC (BUDGET SCENARIO) ===")
for i in range(1, RUNS + 1):
    agent = Agent(
        name="budget_audit_without_ptc_compare",
        model="openai/gpt-5.2",
        instruction=(
            "You are a finance audit assistant. "
            "You must audit all Engineering team members end-to-end. "
            "Important: call exactly one tool per assistant turn. "
            "Do not batch multiple tool calls in one turn. "
            "Use get_team_members(department='Engineering'), then for each member call get_expenses(user_id, quarter='Q3'), "
            "then call get_budget_by_level(level). "
            "Team members are at team_result['data']['members']. "
            "Compute totals and return only members who exceeded budget sorted by overage descending. "
            "Do not skip members and do not estimate."
        ),
        tools=[GetTeamMembersTool(), GetExpensesTool(), GetBudgetByLevelTool()],
    )

    start = perf_counter()
    result = agent.run(QUERY, local=True, trace=True, verbose=False)
    wall = perf_counter() - start

    llm_steps = sum(1 for step in result.steps if step.kind == "agent_thinking_step")
    without_duration.append(result.duration_seconds)
    without_wall.append(wall)
    without_tokens.append(result.total_tokens)
    without_llm_steps.append(llm_steps)

    print(
        f"run {i}: duration={result.duration_seconds:.2f}s, "
        f"wall={wall:.2f}s, total_tokens={result.total_tokens}, llm_steps={llm_steps}"
    )
    if SHOW_RESPONSES:
        print(f"response: {result.text}\n")

print("\n=== WITH PTC (BUDGET SCENARIO) ===")
for i in range(1, RUNS + 1):
    agent = Agent(
        name="budget_audit_with_ptc_compare",
        model="openai/gpt-5.2",
        instruction=(
            "You are a finance audit assistant. "
            "Always use execute_ptc_code for this workflow. "
            "Call execute_ptc_code exactly once and do all looping/aggregation inside that single code execution. "
            "Inside execute_ptc_code: "
            "(1) call get_team_members(department='Engineering'), "
            "(2) read members from team_result['data']['members'], then loop and call get_expenses(user_id=member['id'], quarter='Q3'), "
            "(3) call get_budget_by_level(level=member['level']), "
            "(4) sum expense item amounts in code and compute overage. "
            "Use expense response at result['data']['items'] and budget response at result['data']['quarterly_budget']. "
            "Return only exceeded members sorted by overage descending. "
            "Write defensive code that validates status=='ok' before accessing fields."
        ),
        tools=[GetTeamMembersTool(), GetExpensesTool(), GetBudgetByLevelTool()],
        ptc=PTC(enabled=True, sandbox_timeout=180.0),
    )

    start = perf_counter()
    result = agent.run(QUERY, local=True, trace=True, verbose=False)
    wall = perf_counter() - start

    llm_steps = sum(1 for step in result.steps if step.kind == "agent_thinking_step")
    with_duration.append(result.duration_seconds)
    with_wall.append(wall)
    with_tokens.append(result.total_tokens)
    with_llm_steps.append(llm_steps)

    print(
        f"run {i}: duration={result.duration_seconds:.2f}s, "
        f"wall={wall:.2f}s, total_tokens={result.total_tokens}, llm_steps={llm_steps}"
    )
    if SHOW_RESPONSES:
        print(f"response: {result.text}\n")

without_avg_duration = sum(without_duration) / len(without_duration)
without_avg_wall = sum(without_wall) / len(without_wall)
without_avg_tokens = sum(without_tokens) / len(without_tokens)
without_avg_llm_steps = sum(without_llm_steps) / len(without_llm_steps)

with_avg_duration = sum(with_duration) / len(with_duration)
with_avg_wall = sum(with_wall) / len(with_wall)
with_avg_tokens = sum(with_tokens) / len(with_tokens)
with_avg_llm_steps = sum(with_llm_steps) / len(with_llm_steps)

duration_delta = 0.0
wall_delta = 0.0
token_delta = 0.0
llm_steps_delta = 0.0
if without_avg_duration != 0:
    duration_delta = ((with_avg_duration - without_avg_duration) / without_avg_duration) * 100
if without_avg_wall != 0:
    wall_delta = ((with_avg_wall - without_avg_wall) / without_avg_wall) * 100
if without_avg_tokens != 0:
    token_delta = ((with_avg_tokens - without_avg_tokens) / without_avg_tokens) * 100
if without_avg_llm_steps != 0:
    llm_steps_delta = ((with_avg_llm_steps - without_avg_llm_steps) / without_avg_llm_steps) * 100

print("\n=== SUMMARY ===")
print(
    f"without_ptc: avg_duration={without_avg_duration:.2f}s, "
    f"avg_wall={without_avg_wall:.2f}s, avg_total_tokens={without_avg_tokens:.1f}, "
    f"avg_llm_steps={without_avg_llm_steps:.1f}"
)
print(
    f"with_ptc:    avg_duration={with_avg_duration:.2f}s, "
    f"avg_wall={with_avg_wall:.2f}s, avg_total_tokens={with_avg_tokens:.1f}, "
    f"avg_llm_steps={with_avg_llm_steps:.1f}"
)

print("\n=== DELTA (with_ptc vs without_ptc) ===")
print(f"duration: {duration_delta:.1f}%")
print(f"wall: {wall_delta:.1f}%")
print(f"total_tokens: {token_delta:.1f}%")
print(f"llm_steps: {llm_steps_delta:.1f}%")
