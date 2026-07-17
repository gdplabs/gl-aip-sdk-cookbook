"""Skills Local Path — Use Skill.from_path() to avoid GitHub rate limits."""

from dotenv import load_dotenv

from glaip_sdk import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig
from glaip_sdk.skills import Skill

load_dotenv()

agent = Agent(
    name="skills-local-path-agent",
    instruction="You are a helpful assistant. Use the code-reviewer skill when asked to review code.",
    model="openai/gpt-5.4",
    skills=[Skill.from_path(".agents/skills/code-reviewer")],
    filesystem=LocalDiskConfig(base_directory="~/.workspace/skills-local-path-agent", allow_execute=True),
)

print(agent.run("Please review this code using the code-reviewer skill:\n\n```python\ndef get_user(id):\n    conn = sqlite3.connect('db.sqlite')\n    return conn.execute(f\"SELECT * FROM users WHERE id = {id}\").fetchone()\n```", verbose=True, local=True))
