"""Hello World - Multi-Agent Example with Subagents."""

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from glaip_sdk.agents import Agent


class GetWeatherTool(BaseTool):
    name: str = "get_weather"
    description: str = "Get the current weather for a city"
    args_schema: type[BaseModel] = type("WeatherInput", (BaseModel,), {"city": Field(description="City name")})

    def _run(self, city: str) -> str:
        return f"Weather in {city}: Sunny, 25°C"


class AddTool(BaseTool):
    name: str = "add_numbers"
    description: str = "Add two numbers together"
    args_schema: type[BaseModel] = type("AddInput", (BaseModel,), {"a": Field(description="First number"), "b": Field(description="Second number")})

    def _run(self, a: int, b: int) -> str:
        return f"{a} + {b} = {a + b}"


weather_agent = Agent(
    name="weather_agent",
    instruction="You are a weather expert. Use get_weather to answer weather questions.",
    tools=[GetWeatherTool],
)

math_agent = Agent(
    name="math_agent",
    instruction="You are a math expert. Use add_numbers to perform addition.",
    tools=[AddTool],
)

coordinator = Agent(
    name="coordinator",
    instruction="You are a coordinator. Delegate weather questions to weather_agent and math questions to math_agent.",
    agents=[weather_agent, math_agent],
)

coordinator.run("What's the weather in Tokyo and what is 5 + 7?")
