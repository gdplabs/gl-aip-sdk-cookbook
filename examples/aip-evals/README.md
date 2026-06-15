# AIP Evals — Research Agent Evaluation Demo

Demonstrates how to evaluate an AIP agent using the `glaip_sdk.evals` module,
with both **local** and **hosted** execution modes. The agent is a simple
news research agent backed by a single mocked `web_search` tool — no
real search API is needed. Note: model-based metrics (LLM judge) still
require `OPENAI_API_KEY`.

## Prerequisites

- Python 3.12 (the AIP SDK's native binary dependencies ship `cp312` wheels
  only, so this cookbook cannot be run on 3.11)

## Quickstart

```bash
uv sync
cp .env.example .env
# Fill in OPENAI_API_KEY (and optionally AIP_API_URL / AIP_API_KEY)

uv run python 01_local_eval.py
```

## Eval Scripts

| Script | Execution | Description | Requires |
|--------|-----------|-------------|----------|
| `01_local_eval.py` | Local (in-process) | Runs the agent and eval end-to-end on this machine | `OPENAI_API_KEY` |
| `02_remote_eval.py` | Hosted (deployed) | Deploys the agent to the AIP platform, then runs the eval | `OPENAI_API_KEY`, `AIP_API_URL`, `AIP_API_KEY` |

Both scripts use the same test case (`test_cases/01_indonesia_news.yaml`) and
the same four metrics, so you can compare how the same eval behaves across
local and hosted execution.

## The Test Case

A single test case (`tc-indonesia-2026-news`) combines deterministic and
model-based metrics on the query `"Show 5 news from Indonesia in 2026"`:

- **tool_calls** (deterministic) — verifies the agent calls `web_search` with
  a query containing "indonesia" and "2026".
- **response_keywords** (deterministic) — checks the response contains
  `indonesia`, `news`, and `2026`.
- **completeness** (model / LLM judge) — verifies the response contains
  exactly 5 distinct news items, each with a URL link, all from Indonesia 2026.
- **groundedness** (model / LLM judge) — verifies all claims (titles, links,
  dates) are traceable to the `web_search` tool's retrieved results.

## Folder Structure

```
aip-evals/
├── 01_local_eval.py
├── 02_remote_eval.py
├── _shared.py
├── agents/
│   ├── __init__.py
│   └── research_agent.py
├── tools/
│   ├── __init__.py
│   └── web_search_tool.py
├── test_cases/
│   └── 01_indonesia_news.yaml
├── pyproject.toml
└── .env.example
```

## The Agent

`agents/research_agent.py` defines a single `Agent` with a custom LangChain
`BaseTool` (`WebSearchTool`) that returns a fixed set of mocked search results.
This keeps the cookbook self-contained — no real search API needed.

## Adding More Test Cases

Add a new YAML file under `test_cases/` and reference it from an eval script.
Each YAML file is one or more test cases with `input.message` and a list of
`metrics`.

**Deterministic metric example:**
```yaml
- name: tool_calls
  type: deterministic
  reference:
    tool_calls:
      - tool: web_search
        params:
          query:
            match: keyword
            value: ["indonesia"]
```

**Model (LLM judge) metric example:**
```yaml
- name: completeness
  type: model
  threshold: 0.5
  model:
    name: openai/gpt-5.4
    credentials: env:OPENAI_API_KEY
  reference: The final response must present exactly 5 news items with URL links.
```

## More Information

- [Agent Evaluations Guide](https://gdplabs.gitbook.io/sdk/gl-aip-ai-agent-package/guides/agent-evaluations) — full reference for the evals module, metric types, and report format
- [GL AIP Python SDK Reference](https://gdplabs.gitbook.io/gl-aip/getting-started/quick-start-guide/python-sdk) — `AgentEvaluator` API
- [GL AIP Getting Started](https://gdplabs.gitbook.io/gl-aip/getting-started/install-and-configure) — installation and configuration

