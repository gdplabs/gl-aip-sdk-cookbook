"""Aggregator Pattern (Daily Briefing Synthesizer)

This example demonstrates specialists running in parallel with their outputs
aggregated and synthesized using gllm_pipeline.

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
from tools.mock_calendar_tool import MockCalendarTool
from tools.mock_time_tool import MockTimeTool
from tools.mock_weather_tool import MockWeatherTool

load_dotenv(override=True)


class State(BaseModel):
    """Pipeline state for aggregator pattern.

    Attributes:
        time_query: Query for time and calendar information.
        weather_query: Query for weather information.
        time_text: Output from time/calendar agent.
        weather_text: Output from weather agent.
        partials_text: Combined specialist outputs.
        final_answer: Final synthesized answer.
    """

    time_query: str
    weather_query: str
    time_text: str
    weather_text: str
    partials_text: str
    final_answer: str


# Create specialist agents with tools
time_calendar = Agent(
    name="time_calendar",
    instruction="""Use the mock_time tool to get the current time and the mock_calendar tool
to get today's calendar highlights. Be concise.""",
    description="Gets current time and calendar events",
    tools=[MockTimeTool, MockCalendarTool],
    model="openai/gpt-5-mini",
)

weather = Agent(
    name="weather",
    instruction="Use the mock_weather tool to get today's weather forecast. Be concise",
    description="Gets weather forecast",
    tools=[MockWeatherTool],
    model="openai/gpt-5-mini",
)

synth = Agent(
    name="synth",
    instruction="""Synthesize a brief morning briefing from the provided inputs.
Prioritize time-sensitive info, keep it concise and friendly with suggestions.""",
    description="Synthesizes information from multiple sources",
    model="openai/gpt-5-mini",
)

# Create pipeline steps
time_calendar_step = step(
    component=time_calendar.to_component(),
    input_state_map={"query": "time_query"},
    output_state="time_text",
)
weather_step = step(
    component=weather.to_component(),
    input_state_map={"query": "weather_query"},
    output_state="weather_text",
)

run_specialists = parallel(branches=[time_calendar_step, weather_step])


class SpecialistOutputs(TypedDict):
    """Typed dictionary for specialist agent outputs."""

    time_text: str
    weather_text: str


def join_partials(data: SpecialistOutputs) -> str:
    """Join partial outputs from specialist agents.

    Args:
        data: Dictionary containing specialist outputs.

    Returns:
        Formatted string combining time/calendar and weather information.
    """
    return f"Time & Calendar:\n{data['time_text']}\n\nWeather:\n{data['weather_text']}"


join_partials_step = transform(
    operation=join_partials,
    input_states=["time_text", "weather_text"],
    output_state="partials_text",
)

pipeline = (
    run_specialists
    | join_partials_step
    | step(
        component=synth.to_component(),
        input_state_map={"query": "partials_text"},
        output_state="final_answer",
    )
)
pipeline.state_type = State


async def main() -> None:
    """Run the aggregator pattern demo."""
    print("=" * 60)
    print("Aggregator Pattern Demo (Pipeline)")
    print("=" * 60)
    print()
    print("Workflow: Specialists (Parallel) → Aggregator → Synthesizer")
    print("  ⏰ Time/Calendar Agent (with tools)")
    print("  🌤️  Weather Agent (with tool)")
    print("  📋 Synthesizer Agent")
    print()

    # Run the pipeline
    state = State(
        time_query="Get the current time and today's main calendar highlights",
        weather_query="Get today's weather forecast",
        time_text="",
        weather_text="",
        partials_text="",
        final_answer="",
    )
    result = await pipeline.invoke(state)
    print(f"\nDaily Briefing:\n{result['final_answer']}")

    print("\nDemo completed")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
