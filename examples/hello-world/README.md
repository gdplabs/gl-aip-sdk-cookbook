# Hello World - Single Agent

A minimal example demonstrating the simplest way to deploy an agent using direct `Agent()` instantiation.

Note: Commands below assume you run them from this folder unless noted otherwise.

**Pattern:** Config-based `Agent()` instantiation
**Use when:** Simple agents, quick prototypes, one-off deployments

Default run mode in this example is deployment (`agent.deploy()`). If you keep deployment mode, set `AIP_API_URL` and `AIP_API_KEY`.

## Quick Start

1. **Setup environment**

   ```bash
   cp .env.example .env
   # Edit .env with your AIP_API_URL and AIP_API_KEY
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Deploy the agent**

   ```bash
   uv run main.py
   ```

## Hermes Skill (Remote Example)

This folder also includes a remote/deployed Agent Skills example:

- File: `main_with_hermes_skills_remote.py`
- Command: `uv run python main_with_hermes_skills_remote.py`

Required env vars for this flow:

- `AIP_API_URL`
- `AIP_API_KEY`
- `OPENAI_API_KEY`
- `GFORMS`

Optional:

- `GFORMS_SECRET`

Behavior note:

- This script deploys the agent (`agent.deploy()`) and runs via remote mode.
- For local mode without deploy, use
  `examples/hello-world-local/main_with_hermes_skills.py`.

## Project Structure

```
hello-world-single-agent/
├── agents/
│   └── hello_agent.py    # Agent definition
├── tools/
│   └── greeting.py       # Custom LangChain tool
├── main.py               # Entry point
├── pyproject.toml
└── .env.example
```
