"""File discovery: use ls to find files, then read_file to inspect them.

Demonstrates the ls -> read_file discovery pattern where an agent
first explores a directory, then reads specific files that look relevant.

Requires: OPENAI_API_KEY
Run:     uv run python 01_file_discovery.py
"""

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig
from aip_agents.middleware.backends.local_disk import LocalDiskBackend
import tempfile

load_dotenv()

# Create a temp directory and seed files for the agent to discover
with tempfile.TemporaryDirectory() as tmpdir:
    backend = LocalDiskBackend(base_directory=tmpdir)
    backend.write("/workspace/report_q1.md", "# Q1 Report\nRevenue: $100,000\nGrowth: +5%")
    backend.write("/workspace/report_q2.md", "# Q2 Report\nRevenue: $150,000\nGrowth: +50%")
    backend.write("/workspace/data.csv", "month,revenue\nQ1,100000\nQ2,150000")

    agent = Agent(
        name="discovery-agent",
        instruction="You are a helpful assistant with access to a filesystem.",
        filesystem=LocalDiskConfig(base_directory=tmpdir),
    )

    result = agent.run(
        "What's the summary of our Q2 performance? Check the /workspace directory first.",
        local=True,
    )

    print(result)
