"""Hello World - Hermes Skill Example (Google Forms)."""

from __future__ import annotations

from dotenv import load_dotenv

from aip_agents.middleware.skills import SkillConfig
from glaip_sdk.agents import Agent, LocalDiskConfig


SKILL_SOURCE = "https://github.com/raychrisgdp/hermes-skills/tree/d7f2e5da694f2bac3b5014973f1cabe0ae5b4457/google-forms"
QUERY = (
    "Please use the google-forms skill to create a Google Form for a survey about agent skills with exactly these "
    "3 required paragraph questions: 1) How do you mostly use agent skills in your workflow? "
    "2) Which agent skill gives you the most value and why? "
    "3) What is one improvement you want for agent skills? "
    "Please create the form and return only the form edit URL."
)

load_dotenv(override=True)


agent = Agent(
    name="hermes_skill_google-forms",
    instruction="Follow the user query exactly. Do not ask follow-up questions.",
    model="openai/gpt-5.4",
    skills=SkillConfig(skills=[SKILL_SOURCE], auto_read=False),
    filesystem=LocalDiskConfig(base_directory="~/.workspace/hermes-skills-agent", allow_execute=True),
)

print(agent.run(QUERY, verbose=True, local=True))
