import os
from glaip_sdk import Agent
from dotenv import load_dotenv
from aip_agents.tools.gl_connector import GLConnectorTool

from gl_connectors_sdk import GLConnectorToolGenerator

load_dotenv()

os.environ["GL_CONNECTORS_BASE_URL"] = "https://connectors.glair.ai"
github_tool = GLConnectorTool(
    "github_list_issues_tool",
    api_key=os.getenv("GL_CONNECTORS_API_KEY"),
    token=os.getenv("GL_CONNECTORS_USER_TOKEN"),
)

agent = Agent(
    name="aip_with_github_function_call_connector",
    instruction="You are a helpful assistant.",
    tools=[github_tool]
)
response = agent.run("How many issues (all issues, not PRs) are there in https://github.com/github/awesome-copilot?")
print(response)
