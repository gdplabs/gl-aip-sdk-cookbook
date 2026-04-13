"""Codebase analysis: grep across multiple files to find import patterns.

Demonstrates the grep -> read_file -> report workflow.

Requires: OPENAI_API_KEY
Run:     uv run python 04_codebase_analysis.py
"""

from dotenv import load_dotenv
from glaip_sdk.agents import Agent
from glaip_sdk.models.filesystem import LocalDiskConfig
from aip_agents.middleware.backends.local_disk import LocalDiskBackend
import tempfile

load_dotenv()

with tempfile.TemporaryDirectory() as tmpdir:
    backend = LocalDiskBackend(base_directory=tmpdir)
    # Seed a realistic project with 15+ files
    backend.write(
        "/src/auth_service.py",
        "from database import connect_db\nfrom models import User\n\ndef authenticate_user(username, password):\n    conn = connect_db()\n    return conn.query(User).filter_by(username=username).first()\n",
    )
    backend.write(
        "/src/user_repository.py",
        "from database import connect_db\nfrom models import User, Profile\n\nclass UserRepository:\n    def __init__(self):\n        self.conn = connect_db()\n",
    )
    backend.write(
        "/src/config_loader.py",
        "import database\n\ndef load_config():\n    return database.DEFAULT_CONFIG\n",
    )
    backend.write(
        "/src/legacy_imports.py",
        "from database import QueryBuilder\nfrom database import TransactionManager\n",
    )
    backend.write("/src/calculator.py", "def add(a, b):\n    return a + b\n")
    backend.write("/src/string_utils.py", "def truncate(text, length=100):\n    return text[:length]\n")
    backend.write(
        "/tests/test_auth.py",
        "from database import connect_db\nfrom src.auth_service import authenticate_user\n\ndef test_auth():\n    conn = connect_db()\n",
    )
    backend.write(
        "/tests/conftest.py",
        "import pytest\nfrom database import connect_db\n\ndef pytest_configure():\n    conn = connect_db()\n",
    )
    backend.write("/config/database.yml", "host: localhost\nport: 5432\n")
    backend.write("/config/app.json", '{"debug": true}')
    backend.write("/README.md", "# My Application\nUses database module.\n")

    agent = Agent(
        name="codebase-analyzer",
        instruction="You are an expert code analyst. Search efficiently across files and provide comprehensive reports.",
        filesystem=LocalDiskConfig(base_directory=tmpdir),
        model="openai/gpt-5-nano",
    )

    result = agent.run(
        "Analyze the codebase and find all files that import the 'database' module. "
        "Then determine which of those files actually call 'connect_db()'. "
        "Provide a report listing: (1) all files importing database, "
        "(2) which files use connect_db(), and (3) total counts.",
        local=True,
    )

    print(result)
