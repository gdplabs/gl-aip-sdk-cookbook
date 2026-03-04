"""Sequential Multi-Agent System Pattern

This example demonstrates a sequential workflow where agents process data in order.
Output from one agent becomes input to the next using gllm_pipeline.

Usage (from this directory):
    uv run main.py

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from dotenv import load_dotenv
from glaip_sdk import Agent
from gllm_pipeline.steps import step
from pydantic import BaseModel

load_dotenv(override=True)


class State(BaseModel):
    """Pipeline state for sequential pattern.

    Attributes:
        user_query: Original user query.
        refined_query: Refined query from refiner agent.
        final_answer: Final answer from answerer agent.
    """

    user_query: str
    refined_query: str
    final_answer: str


# Sequential workflow: Refiner -> Answerer
refiner = Agent(
    name="refiner",
    instruction="""You are an intent refiner. Given a short or ambiguous user input, rewrite it as a clear, specific,
and well-formed question.
Respond with ONLY the refined question.""",
    description="Refines ambiguous user input into clear questions",
    model="openai/gpt-5-mini",
)

answerer = Agent(
    name="answerer",
    instruction="""You are a helpful coding assistant. Answer concisely.
If the question is about Python, include a minimal code snippet.""",
    description="Answers coding questions with code snippets",
    model="openai/gpt-5-mini",
)

refine_step = step(
    component=refiner.to_component(),
    input_state_map={"query": "user_query"},
    output_state="refined_query",
)
answer_step = step(
    component=answerer.to_component(),
    input_state_map={"query": "refined_query"},
    output_state="final_answer",
)

pipeline = refine_step | answer_step
pipeline.state_type = State


async def main() -> None:
    """Run the sequential example."""
    print("=" * 60)
    print("Sequential Multi-Agent Pattern Demo (Pipeline)")
    print("=" * 60)
    print()
    print("Workflow: Refiner Agent → Answerer Agent")
    print()

    demo_input = "python list to str"
    state = State(user_query=demo_input, refined_query="", final_answer="")
    print(f"Original input: '{demo_input}'")
    print()

    # Run the pipeline
    result = await pipeline.invoke(state)
    print(f"\nFinal answer: {result['final_answer']}")

    print("\nDemo completed")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
