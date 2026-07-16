"""Run multiple chat phases while preserving the conversation history."""

from glaip_sdk.agents import Agent
from dotenv import load_dotenv

load_dotenv(override=True)

ChatHistory = list[dict[str, str]]


def run_chat_turn(agent: Agent, query: str, chat_history: ChatHistory) -> str:
    """Run one query and append its user/assistant turn to ``chat_history``."""
    result = str(agent.run(query, chat_history=chat_history or None, local=True))
    chat_history.extend(
        [
            {"role": "user", "content": query},
            {"role": "assistant", "content": result},
        ]
    )
    return result


def print_phase(number: int, title: str, result: str) -> None:
    """Print a phase heading and its result."""
    print(f"\n=== Phase {number}: {title} ===")
    print(result)


def main() -> None:
    """Run a three-phase conversation with one agent."""
    chat_agent = Agent(
        name="multi_turn_chat_agent",
        instruction="You are a concise and practical planning assistant.",
    )
    chat_history: ChatHistory = []

    breakfast_ideas = run_chat_turn(
        chat_agent,
        "Suggest three healthy breakfast ideas.",
        chat_history,
    )
    print_phase(1, "Collect breakfast ideas", breakfast_ideas)

    meal_plan = run_chat_turn(
        chat_agent,
        "Using the breakfast ideas from my previous message, create a one-day "
        "breakfast and lunch plan. Return only the meal plan with a short "
        "description for each meal.",
        chat_history,
    )
    print_phase(2, "Create a meal plan", meal_plan)

    shopping_list = run_chat_turn(
        chat_agent,
        "Using the meal plan from your previous message, create a concise "
        "shopping list. Group the ingredients by grocery category.",
        chat_history,
    )
    print_phase(3, "Create a shopping list", shopping_list)


if __name__ == "__main__":
    main()
