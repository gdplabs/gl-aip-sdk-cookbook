"""03 - Data Processing Pattern: read → process → write

DEMONSTRATION:
Agent reads CSV data, processes it, and writes a report.

RUN: uv run python 03_data_pipeline.py
"""

from pathlib import Path

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig

from aip_agents.middleware.backends.local_disk import LocalDiskBackend

load_dotenv()


def main():
    data_dir = Path(__file__).parent / "data"
    backend = LocalDiskBackend(base_directory=str(data_dir))

    agent = Agent(
        name="data-analyst",
        instruction="You are a data analyst. Always inspect source data before answering.",
        filesystem=LocalDiskConfig(base_directory=str(data_dir)),
    )

    result = agent.run(
        "Read /workspace/sales_q3.csv, aggregate revenue per channel, "
        "then save a markdown report to /workspace/q99_analysis.md "
        "with channel totals and the grand total.",
        local=True,
    )

    print(result)
    print("\n--- Generated Report ---")
    print(backend.read("/workspace/q99_analysis.md"))


if __name__ == "__main__":
    main()
