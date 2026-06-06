"""03_mixed_eval.py — Mixed Model-Based and Deterministic Metric Example.

Combines model-based (LLM judge) and deterministic metrics for comprehensive evaluation:
- completeness: model-based, chosen because the final response is interpretive
  in nature, making it difficult to capture with keyword-based matching.
- groundedness: model-based, ensures the final response is supported by the
  retrieved context rather than hallucinated.
- tool_calls: deterministic, verifies the agent calls both the SQL query tool
  to retrieve data and the e2b sandbox tool to generate the chart, with proper
  inputs for each.

Requires OPENAI_API_KEY.
Run: uv run python 03_mixed_eval.py
"""

from __future__ import annotations

import os

from _shared import print_json, warn
from agents.lokadata_agent import lokadata_agent
from glaip_sdk.evals import AgentEvaluator


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        warn("Skipping: OPENAI_API_KEY is not set.")
        return

    lokadata_agent.deploy()

    evaluator = AgentEvaluator(name="Lokadata Model Eval", version="1.0.0")
    report = evaluator.evaluate(
        agent=lokadata_agent,
        test_cases="test_cases/03_mixed.yaml",
    )
    print_json(report)


if __name__ == "__main__":
    main()
