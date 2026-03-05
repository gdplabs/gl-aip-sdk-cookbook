# Programmatic Tool Calling

This cookbook includes:

- `main_with_mcp.py`: PTC baseline with MCP integration
- `main_without_ptc.py`: budget-audit scenario without PTC (generic tool-usage instruction)
- `main_with_ptc.py`: same budget-audit scenario with PTC (generic orchestration instruction, not step-by-step handholding)
- `compare_runs_budget.py`: side-by-side benchmark for the same scenario

It shows that you can use MCP and custom tools in one agent:

- MCP tools via `mcps=[...]`
- custom LangChain tools via `tools=[...]`

The comparison scenario is:

> "Which Engineering team members exceeded their Q3 travel budget?"

The answer requires orchestration across three mocked tools:

1. `get_team_members(department)`
2. `get_expenses(user_id, quarter)`
3. `get_budget_by_level(level)`

All tools are mocked LangChain `BaseTool` classes in `tools/` and return a consistent shape:

```json
{
  "status": "ok | not_found",
  "message": "...",
  "data": {}
}
```

Dataset note for this example: `get_expenses(...)["data"]["items"]` already represents the
Q3 travel-expense line items, so totals should sum all `item.amount` values.

Note: Commands below assume you run them from this folder unless noted otherwise.

## Quick Start

1. Setup environment

   ```bash
   cp .env.example .env
   # Edit .env with OPENAI_API_KEY
   # Add E2B_API_KEY when running the PTC script
   ```

2. Install dependencies

   ```bash
   uv sync
   ```

3. Run PTC + MCP baseline

   ```bash
   uv run python main_with_mcp.py
   ```

4. Run without PTC (same budget scenario)

   ```bash
   uv run python main_without_ptc.py
   ```

5. Run with PTC (same budget scenario)

   ```bash
   uv run python main_with_ptc.py
   ```

6. Compare both modes on the same scenario

   ```bash
   uv run python compare_runs_budget.py
   ```

   This scenario uses large raw expense line-items,
   so code execution can aggregate totals before the final answer. It prints duration,
   wall time, token usage, and LLM step count. The non-PTC run is constrained to one
   tool call per turn so round-trip overhead is visible.

   Edit variables at the top of `compare_runs_budget.py` if needed:

   - `QUERY`
   - `RUNS`
   - `SHOW_RESPONSES`

## When PTC Helps (and when not)

PTC is usually beneficial when orchestration is non-trivial:

- many dependent tool calls (step B needs step A output)
- large raw tool payloads that should be pre-aggregated/filter in code
- workflows with loops, conditional branches, and explicit error handling
- cases where reducing LLM round-trips is important

PTC may be unnecessary for simple tasks:

- one small tool call with minimal post-processing
- short two-step flows where normal tool calling is already clear and fast
- scenarios where sandbox startup/exec overhead is larger than orchestration gain

## Project Structure

```
programmatic-tool-calling/
├── tools/
│   ├── __init__.py
│   ├── get_team_members_tool.py
│   ├── get_expenses_tool.py
│   ├── get_budget_by_level_tool.py
├── main_with_mcp.py
├── main_without_ptc.py
├── main_with_ptc.py
├── compare_runs_budget.py
├── pyproject.toml
└── .env.example
```
