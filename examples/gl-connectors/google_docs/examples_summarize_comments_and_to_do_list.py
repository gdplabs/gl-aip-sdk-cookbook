from dotenv import load_dotenv
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

load_dotenv()

DESIRED_TOOLS = { "google_docs_list_documents", # List all documents to find the document id based on the document name
                  "google_docs_get_document", # Get the document to read the content of the document and the comments
                  "google_docs_list_comments", # List all the comments in the document to get the content of the comments
                  "google_docs_summarize_comments", # Summarize the comments to get the main points and action items
                  "google_docs_create_document", # Create a new document to insert the summarized comments and action items into
                  "google_docs_update_document"} # Update the document with the summarized comments and action items

client = LangchainMCPClient({
    "google_docs": {
        "url": f"{os.getenv('GL_CONNECTORS_URL')}/google_docs/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

FILE_NAME= "MCP Testing Report"

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

    prompt = (
        f"Open the document named '{FILE_NAME}'." 
        " Create a new document. The inside of the document should have the summarized comments and structured list of 'Action Items' based on those comments so I know exactly what I need to revise."
        "After that, give me a brief tone analysis—are the reviewers happy or concerned on the document"
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
