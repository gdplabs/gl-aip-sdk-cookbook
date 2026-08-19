# AIP Evals - Employee Lookup Evaluation Demo

This example evaluates the same employee lookup agent in two execution modes:

- `01_local_eval.py` runs the agent with the local `aip-agents` runtime.
- `02_remote_eval.py` deploys the agent and runs it through the hosted AIP API.

Both scripts use the native `gllm-evals` workflow introduced in
`glaip-sdk>=0.8.57`:

1. Load a native suite from `data/`.
2. Materialize agent observations with `agent.create_eval_suites(...)`.
3. Evaluate the materialized suite with `gllm_evals.evaluate_suites(...)`.
4. Store the run with `JSONExperimentTracker` and print the result rows.

The employee directory is mocked and self-contained. The agent and
model-based evaluator require `OPENAI_API_KEY`.

## Prerequisites

- Python 3.12
- `uv`
- `OPENAI_API_KEY`

The remote example also requires `AIP_API_URL` and `AIP_API_KEY`.

## Quickstart

```bash
uv sync
cp .env.example .env
# Fill in OPENAI_API_KEY. For the remote example, also fill in AIP_API_URL
# and AIP_API_KEY.

uv run python 01_local_eval.py
uv run python 02_remote_eval.py
```

Each run writes JSON experiment data under `output/`.

## Suite

`data/employee_lookup.yaml` defines one test case for:

```text
Who are the employees in the Engineering department?
```

The suite expects the agent to call `employee_lookup` for the Engineering
department and return Alice Chen, Bob Smith, and Carol Wu. It uses the native
`gllm-evals` evaluators from the upstream example:

- `DeepEvalToolCorrectnessMetric`
- `GEvalCompletenessMetric`

The completeness metric uses `openai/gpt-4o-mini` and
`${OPENAI_API_KEY}` from the suite configuration.

## Folder Structure

```text
aip-evals/
├── 01_local_eval.py
├── 02_remote_eval.py
├── data/
│   └── employee_lookup.yaml
├── tools/
│   ├── __init__.py
│   └── employee_lookup.py
├── pyproject.toml
└── .env.example
```

Add additional native suite YAML files under `data/`. Both scripts load the
directory, so each new suite is included in local and hosted runs.

## References

- [GL AIP SDK evaluation examples](https://github.com/GDP-ADMIN/glaip-sdk/tree/main/python/glaip-sdk/examples/evaluations)
- [Agent Evaluations Guide](https://gdplabs.gitbook.io/sdk/gl-aip-ai-agent-package/guides/agent-evaluations)
- [GL AIP Python SDK](https://gdplabs.gitbook.io/gl-aip/getting-started/quick-start-guide/python-sdk)
