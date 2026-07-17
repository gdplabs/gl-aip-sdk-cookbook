# Skills Local Path — Avoid GitHub Rate Limits

This example demonstrates how to use **locally uploaded skills** (`Skill.from_path()`) instead of remote GitHub skills. This approach avoids GitHub API rate limiting issues and provides more reliable agent execution.

## Why Local Path Skills?

When agents load skills directly from remote GitHub repositories, they may experience intermittent failures due to GitHub API rate limits. Using local path-based skills:

- **No GitHub API calls** — skills are loaded from the local filesystem
- **Deterministic** — skill content is version-controlled in your repo
- **Works everywhere** — local runs and remote deploys both supported
- **Upload on deploy** — for remote runs, the skill payload is uploaded during `agent.deploy()`

## Prerequisites

- Python 3.11 or 3.12
- `uv` package manager
- `OPENAI_API_KEY` set in your environment or `.env` file

## Quick Start

> **Note:** Run all commands from this directory. `Skill.from_path(".agents/skills/code-reviewer")` resolves relative to the current working directory.

```bash
# 1. Copy and configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 2. Install dependencies
uv sync

# 3. Run the example
uv run python main.py
```

## Project Structure

```
skills-local-path/
├── .python-version
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
├── main.py                          # Entry point — loads skill from local path
└── .agents/
    └── skills/
        └── code-reviewer/
            └── SKILL.md             # The skill definition (local, not remote)
```

## How It Works

Instead of referencing a remote GitHub URL:

```python
# Remote GitHub skill (subject to rate limits)
skills=["https://github.com/org/repo/tree/main/skills/my-skill"]
```

Use `Skill.from_path()` to load from a local directory:

```python
from glaip_sdk.skills import Skill

skill = Skill.from_path(".agents/skills/code-reviewer")

agent = Agent(
    name="skills-local-path-agent",
    instruction="You are a helpful assistant.",
    model="openai/gpt-5.4",
    skills=[skill],
    filesystem=LocalDiskConfig(
        base_directory="~/.workspace/skills-local-path-agent",
        allow_execute=True,
    ),
)
```

## Remote Deploy with Local Path Skills

For remote execution, use the same `Skill.from_path()` pattern — the SDK uploads the skill payload during `agent.deploy()`:

```python
skill = Skill.from_path(".agents/skills/code-reviewer")

agent = Agent(
    name="skills-uploaded-agent",
    instruction="You are a helpful assistant.",
    model="openai/gpt-5.4",
    skills=[skill],
)

agent.deploy()
result = agent.run("Review the code in main.py")
```

## Creating Your Own Skill

1. Create a directory under `.agents/skills/<skill-name>/`
2. Add a `SKILL.md` file with YAML frontmatter (`name`, `description`) and markdown instructions
3. Load it with `Skill.from_path(".agents/skills/<skill-name>")`

See the [Skills documentation](https://gdplabs.gitbook.io/sdk/gl-aip-ai-agent-package/guides/skills#path-based-skills-local-and-remote) for more details.

## Related Examples

- `examples/hello-world-local/main_with_hermes_skills.py` — Remote GitHub skill (local run)
- `examples/hello-world/main_with_hermes_skills_remote.py` — Remote GitHub skill (deployed)
- `examples/gl-connectors-examples/05_aip_with_github_skills_connector.py` — Remote GitHub skill with GL Connectors
