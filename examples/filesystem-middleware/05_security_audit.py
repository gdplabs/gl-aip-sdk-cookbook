"""Security audit: grep for secrets, read suspicious files, produce a risk report.

Demonstrates the multi-step grep -> read_file -> analysis workflow
applied to a security investigation.

Requires: OPENAI_API_KEY
Run:     uv run python 05_security_audit.py
"""

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig
from aip_agents.middleware.backends.local_disk import LocalDiskBackend
import tempfile

load_dotenv()

with tempfile.TemporaryDirectory() as tmpdir:
    backend = LocalDiskBackend(base_directory=tmpdir)
    # Files with hardcoded secrets
    backend.write(
        "/src/database_config.py",
        'DB_PASSWORD = "SuperTestSecret123!"  # HARDCODED\nCONNECTION_URL = "postgresql://admin:SuperTestSecret123!@localhost/db"\n',
    )
    backend.write(
        "/src/api_client.py",
        'API_KEY = "sk_dummy_51H8x9j2K3L4mN5oP6qR7sT"  # HARDCODED\n',
    )
    backend.write(
        "/config/production.yml",
        "database:\n  password: Pr0d_P@ss_2024!\naws:\n  secret_access_key: wJalrXUtnFEMI/K7MDENG\n",
    )
    # Safe files
    backend.write("/src/calculator.py", "def add(a, b):\n    return a + b\n")
    backend.write(
        "/src/validators.py",
        "import re\n\ndef validate_email(email):\n    return bool(re.match(r'^[^@]+@[^@]+$', email))\n",
    )

    agent = Agent(
        name="security-auditor",
        instruction="You are a security auditor. Search for hardcoded credentials, examine suspicious files, and provide a security report with risk levels.",
        filesystem=LocalDiskConfig(base_directory=tmpdir),
        model="openai/gpt-5-nano",
    )

    result = agent.run(
        "Search /workspace for hardcoded credentials: password, api_key, secret. "
        "Examine suspicious files and provide a security report with risk levels "
        "(high/medium/low) and remediation recommendations.",
        local=True,
    )

    print(result)
