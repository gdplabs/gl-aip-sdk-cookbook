import os
from glaip_sdk import Agent, MCP
from dotenv import load_dotenv

load_dotenv()

github_mcp = MCP(
    name="github",
    transport="http",
    config={"url": "https://connectors.glair.ai/github/mcp"},
)
        

agent = Agent(
    name="aip_with_github_mcp_connector",
    instruction="You are a helpful assistant.",
    mcps=[github_mcp],
    mcp_configs={
        github_mcp: {
            "allowed_tools": ["github_list_issues"],
            "authentication": {
                "type": "bearer-token",
                "token": os.getenv("GL_CONNECTORS_USER_TOKEN")
            }
        }
    }
)
response = agent.run("How many issues (all issues, not PRs) are there in https://github.com/github/awesome-copilot?")
print(response)
