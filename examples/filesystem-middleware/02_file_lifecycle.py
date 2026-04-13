"""File lifecycle: create a file, then edit it.

Demonstrates that write_file creates new files (errors if exists)
and edit_file modifies existing files.

Requires: OPENAI_API_KEY
Run:     uv run python 02_file_lifecycle.py
"""

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig
from aip_agents.middleware.backends.local_disk import LocalDiskBackend
import tempfile

load_dotenv()

with tempfile.TemporaryDirectory() as tmpdir:
    backend = LocalDiskBackend(base_directory=tmpdir)

    agent = Agent(
        name="lifecycle-agent",
        instruction="You are a precise documentation assistant.",
        filesystem=LocalDiskConfig(base_directory=tmpdir),
    )

    agent.run(
        "Create a new file at /workspace/notes.md with this content:\n"
        "# Release Notes\nStatus: Draft\nOwner: Platform Team\n",
        local=True,
    )

    result = agent.run(
        "Update /workspace/notes.md: change 'Status: Draft' to 'Status: Final'. "
        "Use edit_file, do not recreate the file.",
        local=True,
    )

    print(result)
    print(backend.read("/workspace/notes.md"))
