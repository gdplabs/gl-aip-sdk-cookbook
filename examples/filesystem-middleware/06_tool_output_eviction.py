"""Tool output eviction: large tool output is auto-saved, agent reads it back.

Demonstrates the auto-eviction workflow where custom tool output exceeding
the default threshold (~80000 chars) is saved to /tool_outputs/, and the
agent uses read_file to access the full data.

Requires: OPENAI_API_KEY
Run:     uv run python 06_tool_output_eviction.py
"""

from pathlib import Path

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig
from langchain_core.tools import tool

load_dotenv()

# Create scratch directory for tool outputs
scratch_dir = Path(__file__).parent / "scratch"
scratch_dir.mkdir(exist_ok=True)


@tool
def fetch_sales_export(region: str) -> str:
    """Fetch a large sales export with enough data to trigger eviction.

    Generates ~500 rows with padding to exceed the default eviction
    threshold of ~80000 characters (20000 tokens).
    """
    lines = ["date,region,channel,amount"]
    for i in range(1, 501):
        amount = 100 + (i % 37) * 3
        channel = ["online", "retail", "enterprise"][i % 3]
        day = (i % 30) + 1
        lines.append(f"2025-10-{day:02d},{region},{channel},{amount}")
    # Large padding to ensure we exceed the ~80000 char threshold
    padding = "x" * 500
    return "\n".join(line + "," + padding for line in lines)


def main():
    agent = Agent(
        name="eviction-analyst",
        instruction="You are a data analyst. When tool output is auto-saved to a file path, use read_file to read it. Always access the full file, not the preview.",
        filesystem=LocalDiskConfig(base_directory=str(scratch_dir)),
        tools=[fetch_sales_export],
        model="openai/gpt-5-nano",
    )

    result = agent.run(
        "Fetch the APAC sales export and tell me the amount and channel in row 250. "
        "If the data was auto-saved, read the file to get the actual values.",
        local=True,
    )

    print(result)


if __name__ == "__main__":
    main()
