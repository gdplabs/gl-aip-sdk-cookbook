from dotenv import load_dotenv
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

load_dotenv()

DESIRED_TOOLS = {"google_docs_create_document", # Create a new document to insert the markdown content into
                 "google_docs_update_document", # Update the document with the markdown content, this tool can handle markdown formatting
                 "google_docs_update_document_markdown", # Tool which is specifically designed to handle markdown content and will ensure the formatting is correct
                 "google_docs_get_document" # Get the document to check if the markdown content has been inserted correctly
                 }

client = LangchainMCPClient({
    "google_docs": {
        "url": f"{os.getenv('GL_CONNECTORS_URL')}/google_docs/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

FILE_NAME= "Tech Stack Proposal for Car Rental Platform"
MARKDOWN_FILE_PATH = os.path.join(os.path.dirname(__file__), "examples_add_markdown.md")

def _load_markdown_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def extract_content(chunk) -> str | None:
    if isinstance(chunk, str):
        return chunk
    if isinstance(chunk, dict):
        return chunk.get("content")
    return getattr(chunk, "content", None)


async def main():
    all_tools = await client.get_tools("google_docs")
    tools = [t for t in all_tools if t.name in DESIRED_TOOLS]

    agent = Agent(
        name="google_docs_agent",
        instruction="You are a helpful assistant.",
        tools=tools,
        model="gpt-5", # Use gpt-5 because it has better reasoning capabilities to understand the instruction and use the tool correctly
    )
    
    # Load the markdown from the local .md file and include its text in the prompt
    markdown_text = _load_markdown_file(MARKDOWN_FILE_PATH)

    prompt = (
        f"I need you to perform three steps:\n"
        f"1. Create a new Google Doc titled '{FILE_NAME}'.\n"
        f"2. Insert the content below into that document.\n\n"
        f"3. Make sure the headers, table, and bullet points are formatted correctly.\n\n"
        f"CONTENT TO INSERT:\n"
        f"--- \n{markdown_text}\n ---"
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
