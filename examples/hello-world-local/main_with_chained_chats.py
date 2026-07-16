"""Hello World - Pass one chat result into a second chat."""

from glaip_sdk.agents import Agent


chat_agent = Agent(
    name="chained_chat_agent",
    instruction="You are a concise and practical planning assistant.",
)

first_query = "Suggest three healthy breakfast ideas."
first_result = str(chat_agent.run(first_query, local=True))

chat_history = [
    {"role": "user", "content": first_query},
    {"role": "assistant", "content": first_result},
]
second_query = """Using the suggestions from my previous message, create a one-day
breakfast and lunch plan. Return only the meal plan with a short description
for each meal."""
second_result = str(chat_agent.run(second_query, chat_history=chat_history, local=True))

print("First chat:")
print(first_result)
print("\nSecond chat (using the first result):")
print(second_result)
