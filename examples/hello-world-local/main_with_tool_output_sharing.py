"""Hello World - Single Agent Example with Tool Output Sharing."""

from glaip_sdk.agents import Agent
from tools import GreetingFormatterTool, GreetingGeneratorTool

greeting_agent = Agent(
    name="hello_local_tool_output_sharing",
    instruction="You are a greeting assistant that uses tool output sharing.",
    tools=[GreetingGeneratorTool, GreetingFormatterTool],
    agent_config={"tool_output_sharing": True},
)

greeting_agent.run("Create a greeting for Alice, then format it nicely.")
