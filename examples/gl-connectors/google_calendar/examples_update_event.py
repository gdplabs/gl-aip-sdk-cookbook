from dotenv import load_dotenv
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

load_dotenv()

DESIRED_TOOLS = {"google_calendar_events_list", # Find the event id based on the event name and date
                 "google_calendar_calendarlist_get", # Get the event after getting the event id
                 "google_calendar_events_update", # Use the event id to update the event with new guest list
                 }

client = LangchainMCPClient({
    "google_calendar": {
        "url": f"{os.getenv('GL_CONNECTORS_URL')}/google_calendar/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

EVENT_DATE = "19 February 2026"
EVENT_TIME = "17:00 WIB"
EVENT_NAME = "Daily Sync with Team"
NEW_GUEST = ["example@gmail.com", "example2@gmail.com"]

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
        f"Add another guest in '{EVENT_NAME}' event on {EVENT_DATE}."
        f"The guest is/are {NEW_GUEST}"
        "Notify only the new guest(s) about the update."
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
