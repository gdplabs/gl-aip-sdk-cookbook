from dotenv import load_dotenv
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

load_dotenv()

DESIRED_TOOLS = {"google_calendar_events_insert"} # Create a new event in the calendar with the specified event name, date, time, and guest list

client = LangchainMCPClient({
    "google_calendar": {
        "url": f"{os.getenv('GL_CONNECTORS_URL')}/google_calendar/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

EVENT_DATE = "19 February 2026"
EVENT_TIME = "21:00 WIB"
EVENT_DURATION = "30 minutes"
EVENT_NAME = "Daily Sync with Team"
EVENT_GUEST = ["example@gmail.com", "example2@gmail.com"]

def extract_content(chunk) -> str | None:
    if isinstance(chunk, str):
        return chunk
    if isinstance(chunk, dict):
        return chunk.get("content")
    return getattr(chunk, "content", None)


async def main():
    all_tools = await client.get_tools("google_calendar")
    tools = [t for t in all_tools if t.name in DESIRED_TOOLS]

    agent = Agent(
        name="google_calendar_agent",
        instruction="You are a helpful assistant.",
        tools=tools,
        model="gpt-5", # Use gpt-5 because it has better reasoning capabilities to understand the instruction and use the tool correctly
    )

    prompt = (
        f"Insert an event for {EVENT_DATE} at {EVENT_TIME} with duration of {EVENT_DURATION}."
        f"The event's name is {EVENT_NAME}"
        f"The guests is/are {EVENT_GUEST}"
        "Attach the google meet link"
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
