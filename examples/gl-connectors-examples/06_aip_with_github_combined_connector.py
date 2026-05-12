import os
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from glaip_sdk import Agent, MCP
from glaip_sdk.models.filesystem import LocalDiskConfig
from aip_agents.tools.gl_connector import GLConnectorTool
from gl_connectors_sdk import GLConnectors

load_dotenv()

# --- API Tool (custom LangChain tool using GLConnectors SDK directly) ---
class GitHubListIssuesInput(BaseModel):
    owner: str = Field(..., description="The owner of the repository")
    repo: str = Field(..., description="The repository name")
    per_page: int = Field(30, ge=1, le=100, description="Results per page (max 100).")
    cursor: str | None = Field(None, description="Pagination cursor from a previous response; omit for the first page.")

class GitHubListIssuesTool(BaseTool):
    name: str = "github_list_issues_api"
    description: str = "List issues from a GitHub repository using the API directly. Supports pagination via cursor."
    args_schema: type[BaseModel] = GitHubListIssuesInput

    def _run(self, owner: str, repo: str, per_page: int = 30, cursor: str | None = None) -> dict[str, Any]:
        connector = GLConnectors(api_base_url="https://connectors.glair.ai")
        params: dict[str, Any] = {"owner": owner, "repo": repo, "per_page": per_page}
        if cursor:
            params["cursor"] = cursor
        data, _ = connector.execute("github", "list_issues", token=os.getenv("GL_CONNECTORS_USER_TOKEN"), input_=params)
        return data

github_api_connector_tool = GitHubListIssuesTool()

# --- GLConnector Tool (pre-built tool from aip_agents) ---
os.environ["GL_CONNECTORS_BASE_URL"] = "https://connectors.glair.ai"
github_function_call = GLConnectorTool(
    "github_list_issues_tool",
    api_key=os.getenv("GL_CONNECTORS_API_KEY"),
    token=os.getenv("GL_CONNECTORS_USER_TOKEN"),
)

# --- MCP Tool ---
github_mcp = MCP(
    name="github",
    transport="http",
    config={"url": "https://connectors.glair.ai/github/mcp"},
)

# --- Skill ---
github_skill = "https://github.com/github/awesome-copilot/tree/main/skills/github-issues"

# --- Agent with API + Function Call + MCP + Skill (same task: list_issues) ---
agent = Agent(
    name="aip_with_github_combined_connector",
    instruction="You are a helpful assistant.",
    tools=[github_api_connector_tool, github_function_call],
    mcps=[github_mcp],
    mcp_configs={
        github_mcp: {
            "allowed_tools": ["github_list_issues"],
            "authentication": {
                "type": "bearer-token",
                "token": os.getenv("GL_CONNECTORS_USER_TOKEN"),
            },
        }
    },
    skills=[github_skill],
    filesystem=LocalDiskConfig(
        base_directory="/tmp/agent_files",
        allow_execute=True,
        env={"gh_token": os.getenv("GITHUB_TOKEN")},
    ),
)

response = agent.run(
    "List all issues in https://github.com/github/awesome-copilot regardless of state, "
    "find the oldest one, then print its full data."
)
print(response)
