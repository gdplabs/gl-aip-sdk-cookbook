from dotenv import load_dotenv
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

load_dotenv()

DESIRED_TOOLS = {"google_drive_search_files", # Search for the file to move based on the file link
                 "google_drive_summarize_total_files_by_type", # Summarize the content of the file to understand what the file is about before moving it to the new folder
                 "google_drive_create_folder", # Create a new folder in root directory
                 "google_drive_copy_file", # Copy the file into the new folder
                 "google_drive_create_permission"} # Create permission for the new folder

client = LangchainMCPClient({
    "google_drive": {
        "url": f"{os.getenv('GL_CONNECTORS_URL')}/google_drive/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

FILE_LINK = "https://docs.google.com/..."
NEW_FOLDER_NAME = "Summarized Files"
EMAIL = ["example@gmail.com","example2@gmail.com"]

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
        f"Search for a specific file link '{FILE_LINK}' and summarize it."
        f"Copy that file into a new folder named '{NEW_FOLDER_NAME}'. "
        f"Finally, create a permission for that new folder so that {EMAIL} can view it."
        " Send me the final link of the folder and the summarized report."
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
