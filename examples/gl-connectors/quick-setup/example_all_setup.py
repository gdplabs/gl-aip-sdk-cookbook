"""Direct execution example for BOSA MCP with pre-configured credentials.

This script demonstrates BOSA MCP usage when all credentials are already
configured in the environment. It assumes you have:
- BOSA_CLIENT_KEY set in your environment
- BOSA_IDENTIFIER and BOSA_USER_SECRET for authentication
- Optional: Existing GitHub integration (will go through the Github Flow if not present)

For interactive setup, use `uv run example_interactive.py` instead.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import asyncio
import os
from typing import cast

from bosa_connectors import BosaConnector
from dotenv import load_dotenv

from mcp import ClientSession
from gllm_tools.mcp.client.session import create_session

load_dotenv()

bosa_api_url = os.getenv("BOSA_API_URL") or "https://api.bosa.id"
bosa_client_key = os.getenv("BOSA_CLIENT_KEY")

bosa_connector = BosaConnector(
    api_base_url=bosa_api_url,
    api_key=bosa_client_key,
)

user_identifier = os.getenv("BOSA_IDENTIFIER")
user_secret = os.getenv("BOSA_USER_SECRET")

bosa_token = bosa_connector.authenticate_bosa_user(user_identifier, user_secret).token

if not bosa_connector.user_has_integration("github", bosa_token):
    create_github_integration = bosa_connector.initiate_connector_auth("github", bosa_token, "http://localhost:8000")
    print(f"3. Or open this URL: {create_github_integration}")
    exit(1)

bosa_configuration = {
    "transport": "streamable_http",
    "url": f"{bosa_api_url}/github/mcp",
    "headers": {
        "Authorization": f"Bearer {bosa_token}",
        "X-Api-Key": bosa_client_key,
    }
}

async def main() -> None:
    async with create_session(bosa_configuration) as session:
        await session.initialize()
        owner = input("  Repository owner (e.g., 'octocat'): ").strip()
        repo = input("  Repository name (e.g., 'Hello-World'): ").strip()
        issue_number_str = input("  Issue number (e.g., '1'): ").strip()
        tool_name = "github_get_issue_handler"
        params = {
            "owner": owner,
            "repo": repo,
            "issue_number": int(issue_number_str),
        }
        request = {"request": params}
        call_tool_result = await cast(ClientSession, session).call_tool(tool_name, request)
        print(call_tool_result)

if __name__ == "__main__":
    asyncio.run(main())
