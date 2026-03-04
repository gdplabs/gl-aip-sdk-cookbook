"""Loop Pattern (Autonomous internal loop via sub-agent delegation)

This example demonstrates an optimization loop where an optimizer agent
iteratively improves code by delegating execution to an executor agent.

Usage (from this directory):
    uv run main.py

Note:
    Requires E2B_API_KEY environment variable for code sandbox functionality.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from dotenv import load_dotenv
from glaip_sdk import Agent
from glaip_sdk.tools import Tool

load_dotenv(override=True)


# Native tool - will be resolved locally from aip_agents.tools
e2b_sandbox_tool = Tool.from_native("e2b_sandbox_tool")

# Executor agent with code sandbox tool
executor_agent = Agent(
    name="executor_agent",
    instruction="""You are an Execution & Benchmark agent.
When given Python code, run it (use your code interpreter tool if available),
measure runtime, check correctness if specified, and return a short plain-text report.""",
    description="Executes and benchmarks Python code",
    tools=[e2b_sandbox_tool],
    model="openai/gpt-5-mini",
)

# Optimizer agent that delegates to executor
optimizer_agent = Agent(
    name="optimizer_agent",
    instruction="""You are an Optimization agent.
You have a sub-agent named 'executor_agent' who can run and benchmark code.
Perform a brief INTERNAL loop (up to 3 iterations): propose code, delegate to 'executor_agent' to run/benchmark,
read the report, refine if needed, then stop.
Finally, return a concise plain-text summary and the final Python code. Include information such as total running time,
final output, total iterations, and final code.""",
    description="Iteratively optimizes code through testing",
    agents=[executor_agent],
    model="openai/gpt-5-mini",
)


def main() -> None:
    """Run the simplified loop example."""
    print("=" * 60)
    print("Loop Pattern (Auto) Demo (Local Execution)")
    print("=" * 60)
    print()
    print("Agent Hierarchy:")
    print("  🔄 Optimizer Agent")
    print("     └── ⚡ Executor Agent (has e2b_sandbox_tool)")
    print()
    print("The optimizer will iterate up to 3 times to optimize the code.")
    print()

    prompt = """Goal: Produce a minimal, correct Python program that count total prime numbers up to 10^6.
Expected output: 78498, with runtime less than 1 seconds. Try from basic approach, then optimize.
Iterate up to 3 times until you satisfy the expected output."""

    print("Task:", prompt[:80] + "...")
    print()
    print("-" * 60)

    # Run the optimizer
    result = optimizer_agent.run(prompt, verbose=False)

    print(result)
    print("\nDemo completed")


if __name__ == "__main__":
    main()
