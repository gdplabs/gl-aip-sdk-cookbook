#!/usr/bin/env python3
"""Evaluate the employee lookup agent locally."""

import asyncio

from dotenv import load_dotenv
from gllm_evals import evaluate_suites
from gllm_evals.experiment_tracker.json_experiment_tracker import JSONExperimentTracker

from tools.employee_lookup import build_employee_lookup_agent


def main() -> None:
    load_dotenv()
    agent = build_employee_lookup_agent()
    suites = agent.create_eval_suites("data", target_mode="local")
    tracker = JSONExperimentTracker(
        project_name="employee-lookup-local",
        output_dir="output",
    )
    asyncio.run(evaluate_suites(suites=suites, experiment_tracker=tracker))


if __name__ == "__main__":
    main()
