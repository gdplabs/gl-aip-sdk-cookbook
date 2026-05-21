# GL Connectors Examples

This project demonstrates the different ways to integrate **GL Connectors** with an AI agent built on `glaip_sdk`. Each example targets the same task — listing GitHub issues of a repository — so you can compare the integration styles side by side: calling the connector API directly, writing your own LangChain tool, using a pre-built function-call tool from `aip_agents`, talking to a remote MCP server, or letting the agent follow an external Skill definition.

All scripts run against [`github/awesome-copilot`](https://github.com/github/awesome-copilot), a public GitHub repository with a healthy backlog of real issues — chosen so every example has actual data to return.

## Prerequisites

- **Python**: `>=3.12, <3.13`
- The `uv` package manager is recommended.
- **Connector integrations**: After logging in to the **[GL Connectors Console](https://connectors.glair.ai/console)**, you must connect the **GitHub** and **Google Drive** integrations before any example will work.

### Connecting Integrations

The examples call connectors on behalf of *your* account, so each connector you use must have an active integration in the console first. Without this step the connector calls will fail (e.g. an unauthorized / missing-integration error).

1. Log in to the **[GL Connectors Console](https://connectors.glair.ai/console)**.
2. Open the **Integrations** section. You will see one card per connector — at minimum **Github** and **Google_drive**.
3. For each of **Github** and **Google_drive**, click **Add New Integration** and complete the OAuth flow.
4. Confirm each one shows an **Active** integration under *Your Integrations* before running the examples.

## Installation

This project manages dependencies using `pyproject.toml`. You can install them by running:

```bash
uv sync
```

## Running the Examples

Every example must be run with `uv run`. For example, to run the first example:

```bash
uv run 01_github_api_connector.py
```

`uv run` executes the script inside this project's virtual environment, so the packages installed by `uv sync` — `glaip_sdk`, `gl_connectors_sdk`, `aip_agents`, and their dependencies — are carried alongside the script. Running the file with a bare `python ...` instead would use your global interpreter, where those packages are not available and the imports will fail. The `**Execution**` line under each example below already uses `uv run` for this reason.

## Environment Variables

Before running the examples, you need to configure your environment variables. Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Populate the following variables inside `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key (required for the `glaip_sdk` Agent to function).
- `GITHUB_TOKEN`: A GitHub Personal Access Token (only required if you intend to run `05_aip_with_github_skills_connector.py` or `06_aip_with_github_combined_connector.py`).
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
| `01_github_api_connector.py` | Direct GL Connectors API call (no agent) | A single `connector.execute(...)` call |
| `02_aip_with_github_api_connector.py` | Custom LangChain tool wrapping the GL Connectors SDK | A full `BaseTool` subclass |
| `03_aip_with_github_function_call_connector.py` | Pre-built `GLConnectorTool` from `aip_agents` | Just the connector name |
| `04_aip_with_github_mcp_connector.py` | Remote MCP server hosted by GL Connectors | An `MCP` config block |
| `05_aip_with_github_skills_connector.py` | External Skill definition + local filesystem | A skill URL + filesystem config |
| `06_aip_with_github_combined_connector.py` | All of the above on a single agent | Everything, for comparison |
| `07_aip_with_pr_summary_pipeline.py` | All four styles, each owning a *different* role | A surgical Drive uploader, Function Calling helpers, MCP, and a local skill |

### 1. `01_github_api_connector.py` — Direct GL Connectors API call
**What it does:** Calls the GL Connectors `github / list_issues` operation directly through the `GLConnectors` SDK — no agent, no LLM, no tool wrapping. The cleanest possible view of what the connector returns. Use this when you just want to invoke a connector from your own code or to sanity-check credentials before plugging it into an agent.
**Execution:** `uv run 01_github_api_connector.py`

### 2. `02_aip_with_github_api_connector.py` — Custom LangChain tool
**What it does:** Hand-rolls a LangChain `BaseTool` (`GitHubListIssuesTool`) that wraps the `GLConnectors` SDK and registers it on a `glaip_sdk` Agent. You define the input schema, the `_run` method, and the call into `connector.execute(...)` yourself. Use this when you want full control over argument validation, error handling, or response shaping.
**Execution:** `uv run 02_aip_with_github_api_connector.py`

### 3. `03_aip_with_github_function_call_connector.py` — Pre-built `GLConnectorTool`
**What it does:** Skips the boilerplate by using `GLConnectorTool` from `aip_agents`. You only supply the connector operation name (`github_list_issues_tool`) and credentials — the tool's schema and execution wiring come for free. Use this when the default behavior of a GL Connectors operation is all you need.
**Execution:** `uv run 03_aip_with_github_function_call_connector.py`

### 4. `04_aip_with_github_mcp_connector.py` — Remote MCP server
**What it does:** Connects the agent to GL Connectors' hosted **Model Context Protocol (MCP)** server over HTTP. Tools are discovered and negotiated at runtime — no local tool classes required. Use this when you want zero local tool code and are happy to let the agent see whatever the MCP server exposes (optionally restricted via `allowed_tools`).
**Execution:** `uv run 04_aip_with_github_mcp_connector.py`

### 5. `05_aip_with_github_skills_connector.py` — External Agent Skill
**What it does:** Points the agent at an external [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) — a directory of markdown instructions and helper files that teaches the agent how to perform a task. This example uses the [`github-issues` skill from `github/awesome-copilot`](https://github.com/github/awesome-copilot/tree/main/skills/github-issues), which instructs the agent to drive the `gh` CLI against your local `GITHUB_TOKEN` from a sandboxed filesystem. Use this when the workflow is best described as a procedure for the agent to follow, rather than a single API call.
**Execution:** `uv run 05_aip_with_github_skills_connector.py`

### 6. `06_aip_with_github_combined_connector.py` — All integrations on one agent
**What it does:** Registers the **same operation** (`github_list_issues`) via every integration method on a single agent, so you can observe which one the LLM picks at runtime:
- A custom LangChain tool (active)
- A pre-built `GLConnectorTool` (active)
- An MCP server connection (active)
- An external Agent Skill backed by a sandboxed filesystem (active)

The agent is prompted to list all issues, find the oldest one, and print its full data. Useful for debugging tool-selection behavior or comparing latencies between styles.
**Execution:** `uv run 06_aip_with_github_combined_connector.py`

### 7. `07_aip_with_pr_summary_pipeline.py` — Four integration styles, four distinct roles
**What it does:** Runs an end-to-end pipeline where each integration style owns a **different** responsibility — the opposite of `06`. The query is `"Summarize PRs from gdplabs/gl-aip-sdk-cookbook within this month."` and the orchestration is driven by a local `example-skill/SKILL.md`. Each style is deliberately matched to the job it is best suited for:
- **API (surgical)** — a custom LangChain tool that calls `GLConnectors.execute("google_drive", "create_file", ...)` with a `ConnectorFile` payload, uploading the report into the caller's My Drive root. *Why API here:* MCP cannot carry binary file uploads, so a direct API call is **necessary** for this step — and it also gives you precise control over the `ConnectorFile` payload and a deterministic result without exposing a broader tool surface to the LLM.
- **Function Calling** — `get_month_date_range`, `write_temp_file`, and `delete_file` for date math and local file lifecycle the LLM otherwise can't do reliably. *Why Function Calling here:* these are small, deterministic, in-process operations with no remote service behind them, so a lightweight local tool is the simplest fit — no API call or MCP server is warranted.
- **MCP** — the GitHub MCP server with `allowed_tools=["github_list_pull_requests"]` — locked to fetching PRs and nothing else. *Why MCP here:* the GitHub connector is already hosted as an MCP server, so there is no local tool code to write or maintain, and `allowed_tools` narrows the surface to exactly the one capability the pipeline needs.
- **Skill (local path)** — `skills=["./example-skill"]` points at a sibling folder containing `SKILL.md`, which defines both the workflow (date window → list PRs → write CSV → upload to Drive → delete temp → respond) and the exact output format. *Why a Skill here:* the orchestration is a multi-step procedure plus an output contract — that is best expressed as instructions for the agent to follow, not as code.

Use this when you want a worked example of composing the integration styles into a real workflow, and a reference for authoring a local `SKILL.md`.
**Execution:** `uv run 07_aip_with_pr_summary_pipeline.py`
