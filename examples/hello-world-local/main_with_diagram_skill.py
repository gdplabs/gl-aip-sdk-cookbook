"""Hello World - Diagram Skill Example."""

from glaip_sdk.agents import Agent, LocalDiskConfig

agent = Agent(
    name="diagram_agent",
    instruction="Follow the user query exactly.",
    model="openai/gpt-5.4",
    skills=["https://github.com/GDP-ADMIN/prompt-template/tree/main/gdp-labs-wide/generic/skills/gdp-labs-diagram"],
    filesystem=LocalDiskConfig(base_directory="~/.workspace/diagram-agent", allow_execute=True),
)

print(
    agent.run(
        "create architecture diagram of the application as per this project in our directory "
        "and make sure to follow all the rules",
        verbose=True,
        local=True,
    )
)
