"""Hello World - Single Agent Example with PII Toggle."""

from glaip_sdk.agents import Agent
from tools import CustomerInfoTool

customer_agent = Agent(
    name="customer_info_agent",
    instruction="You are a helpful assistant that can look up customer info.",
    tools=[CustomerInfoTool],
    agent_config={"enable_pii": True},
)

customer_agent.run("Show customer info for C001.")
