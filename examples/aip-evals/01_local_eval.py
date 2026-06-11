"""01_local_eval.py — Local Execution Eval Example.

Runs the evaluation locally using the in-process aip-agents runtime (no
deployment to the AIP platform required). The agent is executed via
``target_mode="local"`` and runs end-to-end on this machine.

The test case combines deterministic and model-based metrics:
- tool_calls (deterministic): verifies the web_search tool is called.
- response_keywords (deterministic): checks the response contains the
  expected terms ("indonesia", "news", "2026").
- completeness (model): LLM judge verifies the response contains exactly 5
  news items with URL links from Indonesia 2026.
- groundedness (model): LLM judge verifies all claims are traceable to the
  web_search tool's retrieved results.

Requires OPENAI_API_KEY.
Run: uv run python 01_local_eval.py
"""

from __future__ import annotations

import os

from _shared import print_json, warn
from agents.research_agent import research_agent
from glaip_sdk.evals import AgentEvaluator


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        warn("Skipping: OPENAI_API_KEY is not set.")
        return

    evaluator = AgentEvaluator(name="Research Agent Local Eval", version="1.0.0")
    report = evaluator.evaluate(
        agent=research_agent,
        test_cases="test_cases",
        target_mode="local",
    )
    print_json(report)


if __name__ == "__main__":
    main()
