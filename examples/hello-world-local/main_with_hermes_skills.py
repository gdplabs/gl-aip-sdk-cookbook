"""Hello World - Hermes Skill Example (Google Forms)."""

from __future__ import annotations

from dataclasses import dataclass

from aip_agents.middleware.skills import SkillConfig
from glaip_sdk.agents import Agent, LocalDiskConfig


@dataclass(frozen=True)
class SkillCase:
    key: str
    source: str
    query: str


CASE = SkillCase(
    key="google-forms",
    source="https://github.com/raychrisgdp/hermes-skills/tree/eeb2bc37615a4d048a1e9c753963f25cbd7a5582/google-forms",
    query=(
        "I want to create a Google Form for a survey about agent skills with exactly these "
        "3 required paragraph questions: 1) How do you mostly use agent skills in your workflow? "
        "2) Which agent skill gives you the most value and why? "
        "3) What is one improvement you want for agent skills? "
        "Please create the form and return only the form edit URL."
    ),
)


agent = Agent(
    name=f"hermes_skill_{CASE.key}",
    instruction="Follow the user query exactly. Do not ask follow-up questions.",
    model="openai/gpt-5",
    skills=SkillConfig(skills=[CASE.source], auto_read=False),
    filesystem=LocalDiskConfig(base_directory="~/.workspace/hermes-skills-agent", allow_execute=True),
)

print(agent.run(CASE.query, verbose=True, local=True))
