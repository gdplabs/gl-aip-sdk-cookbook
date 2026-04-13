"""Sandbox execution: run Python code in an isolated E2B sandbox.

Demonstrates code execution with SandboxBackend and artifact tracking.

Requires: E2B_API_KEY, OPENAI_API_KEY
Run:     uv run python 07_sandbox_execute.py
"""

import asyncio
import os

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import SandboxConfig
from aip_agents.middleware.tools.execute import ExecuteTool

load_dotenv()

if not os.getenv("E2B_API_KEY"):
    raise RuntimeError("E2B_API_KEY is required")

agent = Agent(
    name="sandbox-executor",
    instruction="You are a Python expert. Execute code to solve problems.",
    filesystem=SandboxConfig(base_dir="/workspace", timeout_seconds=300),
    tools=[ExecuteTool],
)

result = agent.run(
    "Calculate the factorial of 10 using Python and save the result to /workspace/factorial.txt",
    local=True,
)

print(result)
