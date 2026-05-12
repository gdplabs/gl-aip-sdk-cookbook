from dotenv import load_dotenv
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

load_dotenv()

DESIRED_TOOLS = {"google_drive_search_files", # Search for all files in Drive that have the desired name pattern
                 "google_drive_create_folder", # Create a new folder in root directory
                 "google_drive_copy_file"} # Copy the files that match the name pattern into the new folder

client = LangchainMCPClient({
    "google_drive": {
        "url": f"{os.getenv('GL_CONNECTORS_URL')}/google_drive/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

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
        "Search for all files in my Drive that have 'Draft' or 'Untitled' in their name."
        "Create a new folder called 'Unfinished Work' in my root directory, and move (copy then delete original) or just copy those files into that new folder so I can review them later. " 
        "Give me the link to the new folder when done."
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
