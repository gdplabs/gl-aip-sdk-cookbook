import os

from dotenv import load_dotenv
from glaip_sdk import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig

load_dotenv()

GL_CONNECTORS_SKILL = "https://github.com/GDP-ADMIN/prompt-template/tree/f/gl-connectors-skill/gdp-labs-wide/generic/skills/gl-connectors-picker"

# The skill needs these at the agent's runtime; AIP can't inject them itself yet.
CREDENTIAL_VARS = ("GL_CONNECTORS_BASE_URL", "GL_CONNECTORS_TOKEN", "AIP_API_URL", "AIP_API_KEY")

agent_name = os.getenv("AGENT_NAME", "glconnectors-auto-select-tester-unique")

Agent(
    name=agent_name,
    instruction=(
        "You are a friendly AI assistant that can use the gl-connectors skill to "
        "connect to various services to fulfill the user's request. When the user "
        "asks you to add, remove, or adjust capabilities, use the gl-connectors "
        "skill to do so."
    ),
    model="anthropic/claude-sonnet-4-6",
    skills=[GL_CONNECTORS_SKILL],
    filesystem=LocalDiskConfig(
        base_directory="/tmp/workspace",
        allow_execute=True,
        env={
            **{var: os.getenv(var) for var in CREDENTIAL_VARS},
            # The agent can't discover its own name at runtime; the skill reads
            # this to resolve self-referential requests ("give *me* the ability…").
            "AIP_AGENT_NAME": agent_name,
        },
    ),
).deploy()