"""Skills Local Path — Run agents with locally uploaded skills to avoid GitHub rate limits.

This example demonstrates using Skill.from_path() to load a skill from a local
directory instead of fetching it from a remote GitHub repository. This approach:

- Avoids GitHub API rate limiting issues
- Provides deterministic, version-controlled skills
- Works for both local runs and remote deploys (skill is uploaded during deploy)
"""

from dotenv import load_dotenv

from glaip_sdk import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig
from glaip_sdk.skills import Skill

load_dotenv(override=True)

skill = Skill.from_path(".agents/skills/code-reviewer")

agent = Agent(
    name="skills-local-path-agent",
    instruction="You are a helpful assistant. Use the code-reviewer skill when asked to review code.",
    model="openai/gpt-5.4",
    skills=[skill],
    filesystem=LocalDiskConfig(
        base_directory="~/.workspace/skills-local-path-agent",
        allow_execute=True,
    ),
)

QUERY = (
    "Please review the code in this project's main.py file using the code-reviewer skill. "
    "Read the file first, then provide a structured review."
)

print(agent.run(QUERY, verbose=True, local=True))
