# GL Connectors Examples

This project demonstrates the different ways to integrate **GL Connectors** with an AI agent built on `glaip_sdk`. Each example targets the same task — listing GitHub issues / pull requests of a repository — so you can compare the integration styles side by side: writing your own LangChain tool, using a pre-built tool from `aip_agents`, talking to a remote MCP server, or letting the agent follow an external Skill definition.

## Prerequisites

- **Python**: `>=3.12, <3.13`
- The `uv` package manager is recommended.

## Installation

This project manages dependencies using `pyproject.toml`. You can install them by running:

```bash
uv sync
```

## Environment Variables

Before running the examples, you need to configure your environment variables. Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Populate the following variables inside `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key (required for the `glaip_sdk` Agent to function).
- `GITHUB_TOKEN`: A GitHub Personal Access Token (only required if you intend to run the `main_agent_skill.py` or `main_all_combined.py` example).
- `GL_CONNECTORS_API_KEY`: Your master API key for GL Connectors.
- `GL_CONNECTORS_USER_TOKEN`: Your user-specific token for accessing GL Connectors services.

### Obtaining GL Connectors Credentials

1. Navigate to the **[GL Connectors Console](https://connectors.glair.ai/console)**.
2. In the **Credentials** section, you will find two primary keys:
   - **API Key** (in the **Blue** box): Copy this value to your `GL_CONNECTORS_API_KEY`.
   - **User Token** (in the **Green** box): Copy this value to your `GL_CONNECTORS_USER_TOKEN`.

## Project Examples

Each script demonstrates a different integration style for the same underlying capability (listing GitHub issues / pull requests). Pick the one that matches how much of the plumbing you want to own:

| Script | Integration style | What you write |
| --- | --- | --- |
| `main_custom_tool.py` | Custom LangChain tool wrapping the GL Connectors SDK | A full `BaseTool` subclass |
| `main_prebuilt_tool.py` | Pre-built `GLConnectorTool` from `aip_agents` | Just the connector name |
| `main_remote_mcp.py` | Remote MCP server hosted by GL Connectors | An `MCP` config block |
| `main_agent_skill.py` | External Skill definition + local filesystem | A skill URL + filesystem config |
| `main_all_combined.py` | All of the above on a single agent | Everything, for comparison |

### 1. `main_custom_tool.py` — Custom LangChain tool
**What it does:** Hand-rolls a LangChain `BaseTool` (`GitHubListIssuesTool`) that wraps the `GLConnectors` SDK. You define the input schema, the `_run` method, and the call into `connector.execute(...)` yourself. Use this when you want full control over argument validation, error handling, or response shaping.
**Execution:** `uv run main_custom_tool.py`

### 2. `main_prebuilt_tool.py` — Pre-built `GLConnectorTool`
**What it does:** Skips the boilerplate by using `GLConnectorTool` from `aip_agents`. You only supply the connector operation name (`github_list_issues_tool`) and credentials — the tool's schema and execution wiring come for free. Use this when the default behavior of a GL Connectors operation is all you need.
**Execution:** `uv run main_prebuilt_tool.py`

### 3. `main_remote_mcp.py` — Remote MCP server
**What it does:** Connects the agent to GL Connectors' hosted **Model Context Protocol (MCP)** server over HTTP. Tools are discovered and negotiated at runtime — no local tool classes required. Use this when you want zero local tool code and are happy to let the agent see whatever the MCP server exposes (optionally restricted via `allowed_tools`).
**Execution:** `uv run main_remote_mcp.py`

### 4. `main_agent_skill.py` — External Agent Skill
**What it does:** Points the agent at an external [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) — a directory of markdown instructions and helper files that teaches the agent how to perform a task. This example uses the [`github-issues` skill from `github/awesome-copilot`](https://github.com/github/awesome-copilot/tree/main/skills/github-issues), which instructs the agent to drive the `gh` CLI against your local `GITHUB_TOKEN` from a sandboxed filesystem. Use this when the workflow is best described as a procedure for the agent to follow, rather than a single API call.
**Execution:** `uv run main_agent_skill.py`

### 5. `main_all_combined.py` — All integrations on one agent
**What it does:** Registers the **same operation** (`github_list_pull_requests`) via multiple integration methods on a single agent, so you can observe which one the LLM picks at runtime:
- A custom LangChain tool (active)
- A pre-built `GLConnectorTool` (active)
- An MCP server connection (active)

The agent is prompted to list all pull requests, find the oldest one, and print its full data. Useful for debugging tool-selection behavior or comparing latencies between styles.
**Execution:** `uv run main_all_combined.py`
