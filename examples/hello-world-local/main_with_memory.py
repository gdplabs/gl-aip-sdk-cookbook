"""Hello World - Single Agent Example with Memory."""

from glaip_sdk.agents import Agent

memory_agent = Agent(
    name="memory_agent",
    instruction="You are a helpful assistant that remembers information about users.",
    agent_config={"memory": "mem0"},
)

memory_user_id = "user_123"
memory_agent.run("My name is Joan Garcia.", memory_user_id=memory_user_id)
