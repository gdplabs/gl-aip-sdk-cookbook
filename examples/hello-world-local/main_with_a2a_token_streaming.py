"""Hello World - Single Agent Example with A2A Token Streaming."""

from glaip_sdk.agents import Agent

hello_agent = Agent(
    name="hello_streaming_agent",
    instruction="You are a helpful assistant.",
    agent_config={"enable_a2a_token_streaming": True},
)

hello_agent.run("Tell me a short story about a robot learning to paint.")
