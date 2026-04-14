"""04 - Multi-File Search Pattern: grep → read_file

DEMONSTRATION:
Agent searches across multiple files using grep, then reads specific ones.

RUN: uv run python 04_codebase_analysis.py
"""

from pathlib import Path

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig

load_dotenv()


def main():
    data_dir = Path(__file__).parent / "data"

    agent = Agent(
        name="codebase-analyzer",
        instruction="You are an expert code analyst. Search efficiently across files.",
        filesystem=LocalDiskConfig(base_directory=str(data_dir)),
        model="openai/gpt-5-nano",
    )

    result = agent.run(
        "Find all files in /src that import or use 'database'. "
        "For each file found, check if it calls 'connect_db()'. "
        "Report: (1) all files mentioning database, "
        "(2) which call connect_db(), (3) totals.",
        local=True,
    )

    print(result)


if __name__ == "__main__":
    main()
