"""Hello World - Single Agent Example with Chat History."""

from glaip_sdk.agents import Agent
from tools import SimpleGreetingTool

chat_agent = Agent(
    name="chat_history_agent",
    instruction="You are a friendly assistant that remembers our conversation.",
    tools=[SimpleGreetingTool],
)

chat_history = [
    {"role": "user", "content": "Hi! My name is Alice and I love hiking."},
    {"role": "assistant", "content": "Hello Alice! It's great to meet you. Hiking is wonderful!"},
]

chat_agent.run(
    "What outdoor activity do I enjoy?",
    chat_history=chat_history,
)
