"""Comparison for budget-audit scenario focused on correctness and tokens."""

from __future__ import annotations

import json
import re

from dotenv import load_dotenv

from glaip_sdk.agents import Agent
from glaip_sdk.ptc import PTC
from tools import GetBudgetByLevelTool, GetExpensesTool, GetTeamMembersTool

load_dotenv(override=True)

QUERY = "Which Engineering team members exceeded their Q3 travel budget?"
RUNS = 1
SHOW_RESPONSES = False


def compute_expected_exceeded_names() -> list[str]:
    """Compute deterministic ground truth directly from tool outputs."""
    team_tool = GetTeamMembersTool()
    expenses_tool = GetExpensesTool()
    budget_tool = GetBudgetByLevelTool()

    team_result = team_tool._run(department="Engineering")
    if team_result.get("status") != "ok":
        return []

    members = team_result.get("data", {}).get("members", [])
    budget_cache: dict[str, float] = {}
    exceeded: list[tuple[str, float]] = []

    for member in members:
        user_id = member.get("id")
        name = member.get("name")
        level = str(member.get("level", "")).upper()
        if user_id is None or not name or not level:
            continue

        if level not in budget_cache:
            budget_result = budget_tool._run(level=level)
            if budget_result.get("status") != "ok":
                continue

            budget_data = budget_result.get("data", {})
            quarterly_budget = budget_data.get("quarterly_budget")
            if quarterly_budget is None:
                continue
            budget_cache[level] = float(quarterly_budget)

        expenses_result = expenses_tool._run(user_id=user_id, quarter="Q3")
        if expenses_result.get("status") != "ok":
            continue

        items = expenses_result.get("data", {}).get("items", [])
        total = 0.0
        for item in items:
            amount = item.get("amount", 0)
            try:
                total += float(amount)
            except (TypeError, ValueError):
                continue

        overage = total - budget_cache[level]
        if overage > 0:
            exceeded.append((name, overage))

    exceeded.sort(key=lambda x: x[1], reverse=True)
    return [name for name, _ in exceeded]


def parse_prediction(text: str) -> tuple[bool, list[str], int]:
    """Parse strict JSON response with fallback extraction."""
    candidates = [text.strip()]

    fenced = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
    if fenced:
        candidates.append(fenced.group(1).strip())

    json_like = re.search(r"(\{[\s\S]*\})", text)
    if json_like:
        candidates.append(json_like.group(1).strip())

    seen = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)

        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue

        if not isinstance(payload, dict):
            continue

        names = payload.get("exceeded_names")
        count = payload.get("exceeded_count")

        if not isinstance(names, list) or not all(isinstance(x, str) for x in names):
            continue

        normalized_names = [x.strip() for x in names]
        normalized_count = count if isinstance(count, int) else len(normalized_names)
        return True, normalized_names, normalized_count

    return False, [], 0


EXPECTED_NAMES = compute_expected_exceeded_names()
EXPECTED_COUNT = len(EXPECTED_NAMES)

without_tokens: list[int] = []
without_llm_steps: list[int] = []
without_correct: list[bool] = []

with_tokens: list[int] = []
with_llm_steps: list[int] = []
with_correct: list[bool] = []

print("\n=== EXPECTED (GROUND TRUTH) ===")
print(f"exceeded_count={EXPECTED_COUNT}, exceeded_names={EXPECTED_NAMES}")

print("\n=== WITHOUT PTC (BUDGET SCENARIO) ===")
for i in range(1, RUNS + 1):
    agent = Agent(
        name="budget_audit_without_ptc_compare",
        model="openai/gpt-5.2",
        instruction=(
            "You are a finance audit assistant. "
            "You must audit all Engineering team members end-to-end. "
            "For fairness, do not intentionally serialize tool usage. "
            "Batch independent tool calls in the same assistant turn whenever supported by the runtime. "
            "Use get_team_members(department='Engineering') first. Then fetch expenses and budgets for all members, "
            "parallelizing independent calls when possible and avoiding duplicate get_budget_by_level calls for the same level. "
            "Team members are at team_result['data']['members']. "
            "Compute totals and return only members who exceeded budget sorted by overage descending. "
            "Do not skip members and do not estimate. "
            "Final output must be strict JSON only (no markdown, no extra text): "
            '{"exceeded_count": <int>, "exceeded_names": ["name1", "name2"]}.'
        ),
        tools=[GetTeamMembersTool(), GetExpensesTool(), GetBudgetByLevelTool()],
    )

    result = agent.run(QUERY, local=True, trace=True, verbose=False)

    llm_steps = sum(1 for step in result.steps if step.kind == "agent_thinking_step")
    parseable, predicted_names, predicted_count = parse_prediction(result.text)
    is_correct = (
        parseable
        and predicted_count == EXPECTED_COUNT
        and predicted_names == EXPECTED_NAMES
    )

    without_tokens.append(result.total_tokens)
    without_llm_steps.append(llm_steps)
    without_correct.append(is_correct)

    print(
        f"run {i}: total_tokens={result.total_tokens}, llm_steps={llm_steps}, "
        f"parseable={parseable}, correct={is_correct}"
    )
    if not is_correct:
        print(f"  predicted_count={predicted_count}, predicted_names={predicted_names}")
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
            "Write defensive code that validates status=='ok' before accessing fields. "
            "Final output must be strict JSON only (no markdown, no extra text): "
            '{"exceeded_count": <int>, "exceeded_names": ["name1", "name2"]}.'
        ),
        tools=[GetTeamMembersTool(), GetExpensesTool(), GetBudgetByLevelTool()],
        ptc=PTC(enabled=True, sandbox_timeout=180.0),
    )

    result = agent.run(QUERY, local=True, trace=True, verbose=False)

    llm_steps = sum(1 for step in result.steps if step.kind == "agent_thinking_step")
    parseable, predicted_names, predicted_count = parse_prediction(result.text)
    is_correct = (
        parseable
        and predicted_count == EXPECTED_COUNT
        and predicted_names == EXPECTED_NAMES
    )

    with_tokens.append(result.total_tokens)
    with_llm_steps.append(llm_steps)
    with_correct.append(is_correct)

    print(
        f"run {i}: total_tokens={result.total_tokens}, llm_steps={llm_steps}, "
        f"parseable={parseable}, correct={is_correct}"
    )
    if not is_correct:
        print(f"  predicted_count={predicted_count}, predicted_names={predicted_names}")
    if SHOW_RESPONSES:
        print(f"response: {result.text}\n")

without_avg_tokens = sum(without_tokens) / len(without_tokens)
without_avg_llm_steps = sum(without_llm_steps) / len(without_llm_steps)
without_accuracy = (sum(without_correct) / len(without_correct)) * 100

with_avg_tokens = sum(with_tokens) / len(with_tokens)
with_avg_llm_steps = sum(with_llm_steps) / len(with_llm_steps)
with_accuracy = (sum(with_correct) / len(with_correct)) * 100

token_delta = 0.0
llm_steps_delta = 0.0
if without_avg_tokens != 0:
    token_delta = ((with_avg_tokens - without_avg_tokens) / without_avg_tokens) * 100
if without_avg_llm_steps != 0:
    llm_steps_delta = (
        (with_avg_llm_steps - without_avg_llm_steps) / without_avg_llm_steps
    ) * 100

print("\n=== SUMMARY ===")
print(
    f"without_ptc: total_tokens={without_avg_tokens:.1f}, "
    f"llm_steps={without_avg_llm_steps:.1f}, "
    f"accuracy={without_accuracy:.1f}%"
)
print(
    f"with_ptc:    total_tokens={with_avg_tokens:.1f}, "
    f"llm_steps={with_avg_llm_steps:.1f}, "
    f"accuracy={with_accuracy:.1f}%"
)

print("\n=== DELTA (with_ptc vs without_ptc) ===")
print(f"total_tokens: {token_delta:.1f}%")
print(f"llm_steps: {llm_steps_delta:.1f}%")
