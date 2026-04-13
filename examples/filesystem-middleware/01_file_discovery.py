"""01 - File Discovery Pattern: ls → read_file

DEMONSTRATION:
Agent uses ls to discover files, then reads specific ones.

RUN: uv run python 01_file_discovery.py
"""

from pathlib import Path

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig

load_dotenv()

data_dir = Path(__file__).parent / "data"

agent = Agent(
    name="discovery-agent",
    instruction="You are a helpful assistant with access to a filesystem.",
    filesystem=LocalDiskConfig(base_directory=str(data_dir)),
)

result = agent.run(
    "What's the summary of our Q2 performance? Check the /workspace directory first.",
    local=True,
)

print(result)
