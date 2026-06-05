"""01_deterministic_eval.py — Deterministic Metric Example.

Run: uv run python 01_deterministic_eval.py
"""

from __future__ import annotations

from _shared import print_json
from agents.lokadata_agent import lokadata_agent
from glaip_sdk.evals import AgentEvaluator


def main() -> None:
    lokadata_agent.deploy()

    evaluator = AgentEvaluator(name="Lokadata Deterministic Eval", version="1.0.0")
    report = evaluator.evaluate(
        agent=lokadata_agent,
        test_cases="data/lokadata_deterministic.yaml",
    )
    print_json(report)


if __name__ == "__main__":
    main()
