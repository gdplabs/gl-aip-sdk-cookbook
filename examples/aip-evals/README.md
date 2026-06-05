# AIP Evals — Lokadata Agent Evaluation Demo

Demonstrates how to evaluate the Lokadata PDRB data analyst agent using the AIP evals module.

## Quickstart

```bash
uv sync
cp .env.example .env
uv run python 01_deterministic_eval.py
```

## Eval Scripts

| Script | Metric Type | Requires |
|--------|------------|----------|
| `01_deterministic_eval.py` | Deterministic | — |
| `02_model_eval.py` | Model (LLM judge) | `OPENAI_API_KEY` |

## Folder Structure

```
aip-evals-local/
├── 01_deterministic_eval.py
├── 02_model_eval.py
├── _shared.py
├── agents/
│   └── lokadata_agent.py
├── data/
│   ├── lokadata_deterministic.yaml
│   └── lokadata_model.yaml
├── pyproject.toml
└── .env.example
```

## Writing Test Cases

**Deterministic:**
```yaml
- name: tool_calls
  type: deterministic
  reference:
    tool_calls:
      - tool: bosa_sql_query_tool
        output:
          match: keyword
          value: ["PDRB"]
```

**Model (LLM judge):**
```yaml
- name: completeness
  type: model
  threshold: 0.7
  model:
    name: openai/gpt-4o-mini
    credentials: env:OPENAI_API_KEY
  reference: The expected response text.
```
