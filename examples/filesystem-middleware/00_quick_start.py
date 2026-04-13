"""Quick start: filesystem=True shorthand demonstration.

Shows that filesystem=True creates a LocalDiskBackend in a temp directory.
Use explicit LocalDiskConfig(base_directory=path) for persistence.

Requires: OPENAI_API_KEY
Run:     uv run python 00_quick_start.py
"""

from dotenv import load_dotenv
from glaip_sdk.agents import Agent

load_dotenv()

agent = Agent(
    name="quick-start",
    instruction="You are a helpful assistant with access to a filesystem.",
    filesystem=True,  # Shorthand for LocalDiskConfig()
)

result = agent.run(
    "Create a greeting file at /workspace/hello.txt and read it back.",
    local=True,
)

print(result)
