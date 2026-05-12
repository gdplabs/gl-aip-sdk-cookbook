import os
from glaip_sdk import Agent, MCP
from dotenv import load_dotenv
from glaip_sdk.models.filesystem import LocalDiskConfig

load_dotenv()

agent = Agent(
    name="github_agent_api",
    instruction="You are a helpful assistant.",
    skills=["https://github.com/github/awesome-copilot/tree/main/skills/github-issues"],
    filesystem=LocalDiskConfig(
        base_directory="/tmp/agent_files",
        allow_execute=True,
        env={"gh_token": os.getenv("GITHUB_TOKEN")}
    )
)
response = agent.run("How many issues (all issues, not PRs) are there in https://github.com/gdplabs/gl-aip-sdk-cookbook?")
print(response)
