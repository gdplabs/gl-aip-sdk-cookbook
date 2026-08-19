#!/usr/bin/env python3
"""Evaluate the employee lookup agent locally."""

import asyncio

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from gllm_evals import evaluate_suites
from gllm_evals.experiment_tracker.json_experiment_tracker import JSONExperimentTracker

from tools.employee_lookup import EmployeeLookupTool


load_dotenv()
agent = Agent(
    name="employee-lookup-example-agent",
    instruction=(
        "You are an HR assistant. Use the employee_lookup tool to look up employees by "
        "department whenever a user asks who works in a department. Do not answer from memory."
    ),
    description="Example agent that answers HR questions via the employee lookup tool.",
    tools=[EmployeeLookupTool],
)
suites = agent.create_eval_suites("data", target_mode="local")
tracker = JSONExperimentTracker(
    project_name="employee-lookup-local",
    output_dir="output",
)
asyncio.run(evaluate_suites(suites=suites, experiment_tracker=tracker))
