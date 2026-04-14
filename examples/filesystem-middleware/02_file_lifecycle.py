"""02 - File Lifecycle Pattern: write_file → edit_file

DEMONSTRATION:
Agent creates a file, then modifies it with edit_file.

RUN: uv run python 02_file_lifecycle.py
"""

from pathlib import Path

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig

from aip_agents.middleware.backends.local_disk import LocalDiskBackend

load_dotenv()


def main():
    data_dir = Path(__file__).parent / "data"
    workspace_dir = data_dir / "workspace"
    workspace_dir.mkdir(exist_ok=True)

    backend = LocalDiskBackend(base_directory=str(data_dir))

    agent = Agent(
        name="lifecycle-agent",
        instruction="You are a precise documentation assistant.",
        filesystem=LocalDiskConfig(base_directory=str(data_dir)),
    )

    agent.run(
        "Create a new file at /workspace/notes.md with this content:\n"
        "# Release Notes\nStatus: Draft\nOwner: AIP Team\n",
        local=True,
    )

    result = agent.run(
        "Update the status in /workspace/notes.md from Draft to Final.",
        local=True,
    )

    print(result)
    print("\n--- Final file contents ---")
    print(backend.read("/workspace/notes.md"))


if __name__ == "__main__":
    main()
