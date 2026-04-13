"""Data pipeline: read CSV, aggregate, and write a markdown report.

Demonstrates the read -> process -> write workflow.

Requires: OPENAI_API_KEY
Run:     uv run python 03_data_pipeline.py
"""

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig
from aip_agents.middleware.backends.local_disk import LocalDiskBackend
import tempfile

load_dotenv()

with tempfile.TemporaryDirectory() as tmpdir:
    backend = LocalDiskBackend(base_directory=tmpdir)
    # Pre-seed raw data for the agent to process
    backend.write(
        "/workspace/sales_q3.csv",
        "date,channel,revenue\n"
        "2025-07-01,online,300\n"
        "2025-07-01,retail,150\n"
        "2025-07-01,enterprise,450\n"
        "2025-07-02,online,200\n"
        "2025-07-02,retail,100\n"
        "2025-07-02,enterprise,350\n",
    )

    agent = Agent(
        name="data-analyst",
        instruction="You are a data analyst. Always inspect source data before answering.",
        filesystem=LocalDiskConfig(base_directory=tmpdir),
    )

    result = agent.run(
        "Read /workspace/sales_q3.csv, aggregate revenue per channel, "
        "then save a markdown report to /workspace/reports/q3_summary.md "
        "with channel totals and the grand total.",
        local=True,
    )

    print(result)
    print(backend.read("/workspace/reports/q3_summary.md"))
