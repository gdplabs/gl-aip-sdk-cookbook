"""02_remote_eval.py — Remote (Hosted) Execution Eval Example.

Deploys the agent to the AIP platform first, then runs the evaluation against
the hosted agent via ``target_mode="hosted"`` (resolved automatically because
the agent has a deployed identity).

The test case combines deterministic and model-based metrics:
- tool_calls (deterministic): verifies the web_search tool is called.
- response_keywords (deterministic): checks the response contains the
  expected terms ("indonesia", "news", "2026").
- completeness (model): LLM judge verifies the response contains exactly 5
  news items with URL links from Indonesia 2026.
- groundedness (model): LLM judge verifies all claims are traceable to the
  web_search tool's retrieved results.

Requires OPENAI_API_KEY and valid AIP_API_URL / AIP_API_KEY.
Run: uv run python 02_remote_eval.py
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

from _shared import print_json, warn
from agents.research_agent import research_agent
from glaip_sdk.evals import AgentEvaluator


def main() -> None:
    """Deploy the agent, run the eval against the hosted version, and print
    the JSON report.

    Skips with a warning if the required env vars are not set in the
    environment or the local ``.env`` file.
    """
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        warn("Skipping: OPENAI_API_KEY is not set.")
        return
    if not (os.getenv("AIP_API_URL") and os.getenv("AIP_API_KEY")):
        warn("Skipping: AIP_API_URL / AIP_API_KEY are not set.")
        return

    research_agent.deploy()

    evaluator = AgentEvaluator(name="Research Agent Remote Eval", version="1.0.0")
    report = evaluator.evaluate(
        agent=research_agent,
        test_cases="test_cases",
    )
    print_json(report)


if __name__ == "__main__":
    main()
