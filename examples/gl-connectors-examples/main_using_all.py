import os
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from glaip_sdk import Agent, MCP
from aip_agents.tools.gl_connector import GLConnectorTool
from gl_connectors_sdk import GLConnectors

load_dotenv()

# --- API Tool (custom LangChain tool using GLConnectors SDK directly) ---
class GitHubListPullRequestsInput(BaseModel):
    owner: str = Field(..., description="The owner of the repository")
    repo: str = Field(..., description="The repository name")

class GitHubListPullRequestsTool(BaseTool):
    name: str = "github_list_pull_requests_api"
    description: str = "List pull requests from a GitHub repository using the API directly."
    args_schema: type[BaseModel] = GitHubListPullRequestsInput

    def _run(self, owner: str, repo: str) -> dict[str, Any]:
        connector = GLConnectors(api_base_url="https://connectors.glair.ai")
        params = {"owner": owner, "repo": repo}
        data, _ = connector.execute("github", "list_pull_requests", token=os.getenv("GL_CONNECTORS_USER_TOKEN"), input_=params)
        return data

# --- GLConnector Tool (pre-built tool from aip_agents) ---
os.environ["GL_CONNECTORS_BASE_URL"] = "https://connectors.glair.ai"
glcon_tool = GLConnectorTool(
    "github_list_pull_requests_tool",
    api_key=os.getenv("GL_CONNECTORS_API_KEY"),
    token=os.getenv("GL_CONNECTORS_USER_TOKEN"),
)

# --- MCP Tool ---
github_mcp = MCP(
    name="github",
    transport="http",
    config={"url": "https://connectors.glair.ai/github/mcp"},
)

# --- Agent with API + MCP (same tool: list_pull_requests) ---
agent = Agent(
    name="github_agent_all_same_tool",
    instruction="You are a helpful assistant.",
    tools=[GitHubListPullRequestsTool(), glcon_tool],
    mcps=[github_mcp],
    mcp_configs={
        github_mcp: {
            "allowed_tools": ["github_list_pull_requests"],
            "authentication": {
                "type": "bearer-token",
                "token": os.getenv("GL_CONNECTORS_USER_TOKEN"),
            },
        }
    },
)

response = agent.run(
    "List all PRs in https://github.com/gdplabs/gl-aip-sdk-cookbook regardless of state, "
    "find the oldest one, then print its full data."
)
print(response)
