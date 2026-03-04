"""Router Pattern (Hierarchical Routing)

This example demonstrates a router that classifies queries and routes to specialized
agents using gllm_pipeline switch step.

Usage (from this directory):
    uv run main.py

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from dotenv import load_dotenv
from glaip_sdk import Agent
from gllm_pipeline.steps import step, switch
from pydantic import BaseModel

load_dotenv(override=True)


class State(BaseModel):
    """Pipeline state for router pattern.

    Attributes:
        user_query: Original user query.
        route_label: Classification result from router.
        final_answer: Final answer from specialist agent.
        selected_route: The route that was selected.
    """

    user_query: str
    route_label: str
    final_answer: str
    selected_route: str


# Create router and specialist agents
router = Agent(
    name="router",
    instruction="""Classify the language query. Return ONLY one of these labels: spanish | japanese | other
Rules:
- If query mentions 'Spanish', 'español', or Spanish words → return 'spanish'
- If query mentions 'Japanese', 'Japan', or Japanese words → return 'japanese'
- Otherwise → return 'other'""",
    description="Classifies language queries",
    model="openai/gpt-5-mini",
)

spanish = Agent(
    name="spanish",
    instruction="""You are a Spanish language expert teacher.
Provide accurate translations, explanations, and teaching insights.
Respond in a friendly, educational manner.""",
    description="Spanish language expert",
    model="openai/gpt-5-mini",
)

japanese = Agent(
    name="japanese",
    instruction="""You are a Japanese language expert teacher.
Provide accurate translations, explanations, and teaching insights.
Respond in a friendly, educational manner.""",
    description="Japanese language expert",
    model="openai/gpt-5-mini",
)

general = Agent(
    name="general",
    instruction="Politely inform that you can only help with Spanish or Japanese language queries.",
    description="General fallback handler",
    model="openai/gpt-5-mini",
)

# Create pipeline steps
route_step = step(
    component=router.to_component(),
    input_state_map={"query": "user_query"},
    output_state="route_label",
)

spanish_step = step(
    component=spanish.to_component(),
    input_state_map={"query": "user_query"},
    output_state="final_answer",
)
japanese_step = step(
    component=japanese.to_component(),
    input_state_map={"query": "user_query"},
    output_state="final_answer",
)
general_step = step(
    component=general.to_component(),
    input_state_map={"query": "user_query"},
    output_state="final_answer",
)

route_switch = switch(
    condition=lambda s: s["route_label"].strip().lower(),
    branches={
        "spanish": spanish_step,
        "japanese": japanese_step,
        "other": general_step,
    },
    default=general_step,
    output_state="selected_route",
)

pipeline = route_step | route_switch
pipeline.state_type = State


async def main() -> None:
    """Run the router pattern demo."""
    print("=" * 60)
    print("Router Pattern Demo (Pipeline)")
    print("=" * 60)
    print()
    print("Workflow: Router → Switch → Specialist")
    print("  🔀 Router Agent")
    print("     ├── 🇪🇸 Spanish Expert")
    print("     ├── 🇯🇵 Japanese Expert")
    print("     └── 💬 General Handler")
    print()

    # Demo queries
    queries = [
        "How do you say 'love' in Spanish?",
        "What is the meaning of 'arigatou' in English?",
        "How do you say 'hello' in German?",
    ]

    # Process each query
    for query in queries:
        print(f"\n--- Processing Query: {query} ---")
        state = State(user_query=query, route_label="", final_answer="", selected_route="")
        result = await pipeline.invoke(state)
        print(f"Answer: {result['final_answer']}")

    print("\nDemo completed")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
