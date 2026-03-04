"""Hello World - Single Agent Example."""

from glaip_sdk.agents import Agent
from tools import SimpleGreetingTool

hello_agent = Agent(
    name="hello_local_agent",
    instruction="You are a friendly greeting assistant.",
    tools=[SimpleGreetingTool],
)
hello_agent.run("Give me an enthusiastic greeting!")
