from dotenv import load_dotenv
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

load_dotenv()

DESIRED_TOOLS = {"google_drive_recent_files", # Get the most recent files that the user has worked on
                 "google_drive_list_permissions", # List the permissions of the file to find out who has access to the file and what type of access they have
                 "google_drive_update_permission"} # Update the permission of the file to change the access level of a specific user or remove their access

client = LangchainMCPClient({
    "google_drive": {
        "url": f"{os.getenv('GL_CONNECTORS_URL')}/google_drive/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

YOUR_EMAIL = "example@gmail.com"

def extract_content(chunk) -> str | None:
    if isinstance(chunk, str):
        return chunk
    if isinstance(chunk, dict):
        return chunk.get("content")
    return getattr(chunk, "content", None)

async def main():
    all_tools = await client.get_tools("google_drive")
    tools = [t for t in all_tools if t.name in DESIRED_TOOLS]

    agent = Agent(
        name="google_drive_agent",
        instruction="You are a helpful assistant.",
        tools=tools,
        model="gpt-5", # Use gpt-5 because it has better reasoning capabilities to understand the instruction and use the tool correctly
    )

    prompt = (
        "Find the 5 most recent files I've worked on and owned by me."
        "For each of these files, list who has access to them using the permissions tool."
        "If any of them are 'Public' or have 'Anyone with the link' access, "
        f"change their permission to 'Private' but make sure my email {YOUR_EMAIL} remains as the owner with full access."
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
