"""02_model_eval.py — Model (LLM Judge) Metric Example.

Requires OPENAI_API_KEY.
Run: uv run python 02_model_eval.py
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
        test_cases="data/lokadata_model.yaml",
    )
    print_json(report)


if __name__ == "__main__":
    main()
