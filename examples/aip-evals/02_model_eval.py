"""02_model_eval.py — Model (LLM Judge) Metric Example.

Uses an LLM as a judge to evaluate the agent via two model-based metrics:
- completeness: evaluates the final response against the expected answer.
- groundedness: evaluates whether the response is supported by the source/context.

A model-based approach (completeness) is chosen over keyword-based metrics because the
agent's responses contain monetary values that can be formatted differently
(e.g., 18060.62 can be written as 18.060,62, 18,060.62, etc.), making
exact keyword matching unreliable.

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
        test_cases="test_cases/02_mixed.yaml",
    )
    print_json(report)


if __name__ == "__main__":
    main()
