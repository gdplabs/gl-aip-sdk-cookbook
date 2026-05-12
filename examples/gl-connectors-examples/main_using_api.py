import os
from typing import Any

from pydantic import BaseModel, Field

from glaip_sdk.agents import Agent
from langchain_core.tools import BaseTool

from gl_connectors_sdk import GLConnectors

class GitHubListIssuesInput(BaseModel):
    owner: str = Field(..., description="The owner of the repository")
    repo: str = Field(..., description="The repository name")

class GitHubListIssuesTool(BaseTool):
    name: str = "github_list_issues_tool"
    description: str = "Get issues from github repository."
    args_schema: type[BaseModel] = GitHubListIssuesInput

    def _run(self, owner: str, repo: str) -> dict[str, Any]:
        connector = GLConnectors(api_base_url="https://connectors.glair.ai")
        params = {"owner": owner, "repo": repo}
        data, status = connector.execute("github", "list_issues", token=os.getenv("GL_CONNECTORS_USER_TOKEN"), input_=params)
        return data
        

agent = Agent(name="github_agent_api", instruction="You are a helpful assistant.", tools=[GitHubListIssuesTool()])
response = agent.run("How many issues (all issues, not PRs) are there in https://github.com/gdplabs/gl-aip-sdk-cookbook?")
print(response)
