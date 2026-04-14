"""05 - Security Audit Pattern: grep for secrets → risk assessment

DEMONSTRATION:
Agent searches for hardcoded credentials and provides security recommendations.

RUN: uv run python 05_security_audit.py
"""

import re
from pathlib import Path

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig

load_dotenv()


def mask_secrets(text: str) -> str:
    """Mask potential secret values in output."""
    # Mask API keys (sk_... patterns)
    text = re.sub(r"sk_[a-zA-Z0-9_]+", "[REDACTED_API_KEY]", text)
    # Mask passwords after = or :
    text = re.sub(r'(password\s*[=:]\s*)["\']?[^"\'\s]+["\']?', r"\1[REDACTED_PASSWORD]", text, flags=re.IGNORECASE)
    # Mask connection URLs with embedded credentials
    text = re.sub(r"://[^:]+:[^@]+@", "://[REDACTED_CREDENTIALS]@", text)
    return text


def main():
    data_dir = Path(__file__).parent / "data"

    agent = Agent(
        name="security-auditor",
        instruction="You are a security auditor specializing in finding hardcoded credentials. "
        "When you find secrets, describe their location and type but do not repeat the actual secret value. "
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

    # Post-process to ensure secrets are masked in output
    masked_result = mask_secrets(result)
    print(masked_result)


if __name__ == "__main__":
    main()
