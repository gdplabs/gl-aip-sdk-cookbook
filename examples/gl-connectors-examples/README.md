# GL Connectors Examples

This project demonstrates various methods of integrating and utilizing **GL Connectors** with AI Agents, ranging from direct SDK calls to more advanced tool integrations like custom LangChain tools, pre-built `aip_agents` tools, remote MCP servers, and skill files.

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
- `GITHUB_TOKEN`: A GitHub Personal Access Token (only required if you intend to run the `main_using_skill.py` or `main_using_all.py` example).
- `GL_CONNECTORS_API_KEY`: Your master API key for GL Connectors.
- `GL_CONNECTORS_USER_TOKEN`: Your user-specific token for accessing GL Connectors services.

### Obtaining GL Connectors Credentials

1. Navigate to the **[GL Connectors Console](https://connectors.glair.ai/console)**.
2. In the **Credentials** section, you will find two primary keys:
   - **API Key** (in the **Blue** box): Copy this value to your `GL_CONNECTORS_API_KEY`.
   - **User Token** (in the **Green** box): Copy this value to your `GL_CONNECTORS_USER_TOKEN`.

## Project Examples

This project contains several scripts, each showcasing a different way to interact with GL Connectors and GitHub.

### 1. `main.py`
**What it does:** Uses the `GLConnectors` SDK directly via standard asynchronous Python to fetch a list of GitHub issues. It completely bypasses AI agents.
**Execution:** `uv run main.py`

### 2. `main_using_api.py`
**What it does:** Demonstrates how to create a custom LangChain `BaseTool` (`GitHubListIssuesTool`) that wraps the `GLConnectors` SDK. The tool is then provided to an AI agent, which interprets the user's prompt and uses the tool accordingly.
**Execution:** `uv run main_using_api.py`

### 3. `main_using_glcon_tool.py`
**What it does:** Simplifies tool creation by utilizing the pre-built `GLConnectorTool` from the `aip_agents` package. You don't need to write the `_run` boilerplate; you just initialize the tool with the name of the connector service you wish to use (`github_list_issues_tool`) and attach it to the agent.
**Execution:** `uv run main_using_glcon_tool.py`

### 4. `main_using_mcp.py`
**What it does:** Uses the **Model Context Protocol (MCP)** to connect the agent to a remote GL Connectors MCP server. The agent automatically negotiates available tools (like `github_list_issues`) over HTTP without needing local Python tool definitions.
**Execution:** `uv run main_using_mcp.py`

### 5. `main_using_skill.py`
**What it does:** Leverages an external Skill definition file (from GitHub's awesome-copilot repository) and a local filesystem workspace. The agent follows the markdown instructions inside the skill to natively interact with GitHub issues using your local `GITHUB_TOKEN`.
**Execution:** `uv run main_using_skill.py`

### 6. `main_using_all.py`
**What it does:** Registers the **same operation** (`github_list_pull_requests`) via multiple integration methods on a single agent, to observe which one the LLM chooses at runtime:
- A Custom API Tool (active)
- A pre-built `GLConnectorTool` (commented out, can be re-enabled)
- An MCP Server connection (active)

The agent is given a prompt to list all pull requests, find the oldest one, and print its full data.
**Execution:** `uv run main_using_all.py`
