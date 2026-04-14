"""05 - Security Audit Pattern: grep for secrets → risk assessment

DEMONSTRATION:
Agent searches for hardcoded credentials and provides security recommendations.

RUN: uv run python 05_security_audit.py
"""

from pathlib import Path

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig

load_dotenv()


def main():
    data_dir = Path(__file__).parent / "data"

    agent = Agent(
        name="security-auditor",
        instruction="You are a security auditor specializing in finding hardcoded credentials. "
        "Redact actual secret values in your response (show them as [REDACTED]). "
        "Provide specific remediation advice for each finding.",
        filesystem=LocalDiskConfig(base_directory=str(data_dir)),
        model="openai/gpt-5-nano",
    )

    result = agent.run(
        "Perform a security audit of the directory. "
        "Search for hardcoded credentials: password, api_key, secret, token. "
        "For each finding, classify risk (HIGH/MEDIUM/LOW) "
        "and provide specific remediation.",
        local=True,
    )

    print(result)


if __name__ == "__main__":
    main()
