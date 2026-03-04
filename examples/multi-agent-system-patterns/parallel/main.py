"""Parallel Multi-Agent Pattern

This example demonstrates parallel execution where specialist agents work simultaneously,
and their outputs are combined while preserving each agent's distinct perspective.

Usage (from this directory):
    uv run main.py

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from typing import TypedDict

from dotenv import load_dotenv
from glaip_sdk import Agent
from gllm_pipeline.steps import parallel, step, transform
from pydantic import BaseModel

load_dotenv(override=True)


class State(BaseModel):
    """Pipeline state for parallel pattern.

    Attributes:
        user_query: Original user query.
        logistics_out: Output from logistics specialist.
        activities_out: Output from activities specialist.
        combined_output: Combined specialist outputs formatted for display.
    """

    user_query: str
    logistics_out: str
    activities_out: str
    combined_output: str


# Create specialist agents
logistics = Agent(
    name="logistics",
    instruction="""You are a logistics specialist. Focus ONLY on travel logistics like flights, hotels, transport.
Be brief. Do not ask user for clarification, just provide the answer.""",
    description="Handles travel logistics planning",
    model="openai/gpt-5-mini",
)

activities = Agent(
    name="activities",
    instruction="""You are an activities specialist. Focus ONLY on things to do, attractions, food.
Be brief. Do not ask user for clarification, just provide the answer.""",
    description="Handles activities and attractions planning",
    model="openai/gpt-5-mini",
)

# Create pipeline steps
logistics_step = step(
    component=logistics.to_component(),
    input_state_map={"query": "user_query"},
    output_state="logistics_out",
)
activities_step = step(
    component=activities.to_component(),
    input_state_map={"query": "user_query"},
    output_state="activities_out",
)

run_specialists = parallel(branches=[logistics_step, activities_step])


class SpecialistOutputs(TypedDict):
    """Typed dictionary for specialist agent outputs."""

    logistics_out: str
    activities_out: str


def format_specialist_outputs(data: SpecialistOutputs) -> str:
    """Format outputs from specialist agents.

    Args:
        data: Dictionary containing specialist outputs.

    Returns:
        Formatted string combining logistics and activities information.
    """
    return f"[Logistics]\n{data['logistics_out']}\n\n[Activities]\n{data['activities_out']}"


merge_outputs = transform(
    operation=format_specialist_outputs,
    input_states=["logistics_out", "activities_out"],
    output_state="combined_output",
)

pipeline = run_specialists | merge_outputs
pipeline.state_type = State


async def main() -> None:
    """Run the parallel pattern demo."""
    print("=" * 60)
    print("Parallel Multi-Agent Pattern Demo (Pipeline)")
    print("=" * 60)
    print()
    print("Workflow: Specialists (Parallel) → Merge")
    print("  🚗 Logistics Agent")
    print("  🎯 Activities Agent")
    print()

    query = "Plan a 5-day trip to Tokyo"
    state = State(user_query=query, logistics_out="", activities_out="", combined_output="")
    print(f"Query: '{query}'")
    print()

    # Run the pipeline
    result = await pipeline.invoke(state)
    print(f"\nSpecialist Outputs:\n{result['combined_output']}")

    print("\nDemo completed!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
