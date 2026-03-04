"""Hello World - Single Agent Example with Local File Access."""

from pathlib import Path

from glaip_sdk.agents import Agent
from tools import LocalTextFileTool

file_agent = Agent(
    name="hello_local_file_agent",
    instruction="You are a helpful assistant with access to local files.",
    tools=[LocalTextFileTool],
)

base_dir = Path(__file__).resolve().parent
local_file = base_dir / "files" / "hello_local.txt"
file_agent.run("Please read the provided local file and summarize it.", files=[str(local_file)])
