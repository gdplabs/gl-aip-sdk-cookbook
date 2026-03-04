"""Hello World - Multi-Agent Example with Coordinator."""

from glaip_sdk.agents import Agent
from agents import formal_greeter, casual_greeter

greeting_coordinator = Agent(
    name="greeting_coordinator",
    instruction="You are a coordinator that directs greeting specialists to create personalized greetings.",
    description="Coordinates greeting specialists for personalized greetings",
    agents=[formal_greeter, casual_greeter],
)

greeting_coordinator.deploy()
greeting_coordinator.run("Hello, who are you?")
