# Hello World - Local Agent Execution

This example demonstrates how to run a glaip-sdk agent **locally** without deploying to the AIP server.

Note: Commands below assume you run them from this folder unless noted otherwise.

## Features

- 🏠 **Local Execution**: Runs directly on your machine using aip-agents
- ⚡ **No Deploy Required**: Just define and run - no server needed
- 🔧 **Quick Prototyping**: Perfect for development and testing
- 🛠️ **Tool Support**: LangChain BaseTool classes work locally!

## Prerequisites

This example runs in local mode and does **not** require `AIP_API_KEY` or `AIP_API_URL`.

### Base Installation

Install all dependencies using `uv sync`:

```bash
uv sync
```

This will:

- Set up authentication for private repositories (requires `gcloud auth login`)
- Sync all dependencies including `glaip-sdk[local]` and required extras
- Set up the virtual environment with all necessary packages

**Alternative installation methods:**

```bash
# Using pip
pip install "glaip-sdk[local]"

# Using uv directly
uv sync
```

### Required Environment Variables

**Minimum Required (for all examples):**

- `OPENAI_API_KEY`: Required for LLM provider (or configure other LLM provider in aip-agents)

**Example-Specific Environment Variables:**

| Example | Required Environment Variables | Notes |
|---------|------------------------------|-------|
| `main_with_memory.py` | `MEM0_API_KEY` or `GLLM_MEMORY_API_KEY` | Either one works |
| `main_with_native_tool.py --serper` | `SERPER_API_KEY` | Google Serper web search API key |
| `main_with_native_tool.py --e2b` | `E2B_API_KEY` | E2B code sandbox API key |
| `main_with_native_tool.py --browser` | None | Browser Use tool doesn't require API key |
| `main_with_gl_connectors_tool.py` | `GL_CONNECTORS_BASE_URL`<br>`GL_CONNECTORS_API_KEY`<br>`GL_CONNECTORS_USERNAME`<br>`GL_CONNECTORS_PASSWORD`<br>`GL_CONNECTORS_IDENTIFIER` (optional) | GL Connectors configuration (backward compatible with BOSA_*) |
| `main_with_mcp.py`<br>`main_with_agent_definition_configs.py`<br>`main_with_runtime_config.py` | `ARXIV_MCP_API_KEY`<br>`ARXIV_MCP_AUTH_TOKEN` | Optional, for Arxiv MCP server |

**Setting Environment Variables:**

You can set environment variables in two ways:

**Option 1: Export in shell**

```bash
export OPENAI_API_KEY="your-key-here"
export MEM0_API_KEY="your-mem0-key"  # For memory example
export SERPER_API_KEY="your-serper-key"  # For native tools example
export E2B_API_KEY="your-e2b-key"  # For native tools example
export GL_CONNECTORS_BASE_URL="https://your-gl-connector-url"  # For GL Connectors
export GL_CONNECTORS_API_KEY="your-api-key"
export GL_CONNECTORS_USERNAME="your-username"
export GL_CONNECTORS_PASSWORD="your-password"
```

**Option 2: Create a `.env` file** (recommended)

Create a `.env` file in this directory by copying `.env.example`:

```bash
cp .env.example .env
# Then edit .env with your actual API keys
```

**Note**: All examples use `python-dotenv` to automatically load `.env` files. See the "Required Env Vars" column in the examples table below for specific requirements per example.

## Usage

All examples can be run using `uv run` or `python`:

```bash
# Using uv (recommended)
uv run python <example_file>.py

# Using python directly
python <example_file>.py
```

## Available Examples & Commands

> **Prerequisites**: Run `uv sync` first to install all dependencies. All examples below assume dependencies are already installed.

| Example File | Command | Description | Required Env Vars |
|-------------|---------|-------------|------------------|
| **Basic Examples** | | | |
| `main.py` | `uv run python main.py` | Basic local agent execution with greeting tool | `OPENAI_API_KEY` |
| `main_with_chat_history.py` | `uv run python main_with_chat_history.py` | Agent with chat history context | `OPENAI_API_KEY` |
| `main_with_local_files.py` | `uv run python main_with_local_files.py` | Agent with local file access | `OPENAI_API_KEY` |
| `main_with_docproc_pdf.py` | `uv run python main_with_docproc_pdf.py` | Agent with PDF document processing (PDFReaderTool) | `OPENAI_API_KEY` |
| **Configuration Examples** | | | |
| `main_with_agent_definition_configs.py` | `uv run python main_with_agent_definition_configs.py` | Agent with definition configs (tool_configs, agent_config, mcp_configs) | `OPENAI_API_KEY`<br>`ARXIV_MCP_API_KEY` (optional)<br>`ARXIV_MCP_AUTH_TOKEN` (optional) |
| `main_with_runtime_config.py` | `uv run python main_with_runtime_config.py` | Agent with runtime configuration | `OPENAI_API_KEY`<br>`ARXIV_MCP_API_KEY` (optional)<br>`ARXIV_MCP_AUTH_TOKEN` (optional) |
| `main_with_pii_toggle.py` | `uv run python main_with_pii_toggle.py` | Agent with PII redaction toggle | `OPENAI_API_KEY`<br>`NER_API_KEY` (optional)<br>`NER_API_URL` (optional) |
| **Advanced Features** | | | |
| `main_with_hitl.py` | `uv run python main_with_hitl.py` | Agent with human-in-the-loop approval | `OPENAI_API_KEY` |
| `main_with_memory.py` | `uv run python main_with_memory.py` | Agent with mem0 memory backend | `OPENAI_API_KEY`<br>`MEM0_API_KEY` or `GLLM_MEMORY_API_KEY` |
| `main_with_subagents.py` | `uv run python main_with_subagents.py` | Agent with subagents | `OPENAI_API_KEY` |
| `main_with_tool_output_sharing.py` | `uv run python main_with_tool_output_sharing.py` | Agent with tool output sharing | `OPENAI_API_KEY` |
| `main_with_a2a_token_streaming.py` | `uv run python main_with_a2a_token_streaming.py` | Agent with A2A token streaming | `OPENAI_API_KEY` |
| **Integration Examples** | | | |
| `main_with_mcp.py` | `uv run python main_with_mcp.py` | Agent with MCP (Model Context Protocol) integration | `OPENAI_API_KEY`<br>`ARXIV_MCP_API_KEY` (optional)<br>`ARXIV_MCP_AUTH_TOKEN` (optional) |
| `main_with_gl_connectors_tool.py` | `uv run python main_with_gl_connectors_tool.py` | Agent using GL Connectors | `OPENAI_API_KEY`<br>`GL_CONNECTORS_BASE_URL`<br>`GL_CONNECTORS_API_KEY`<br>`GL_CONNECTORS_USERNAME`<br>`GL_CONNECTORS_PASSWORD`<br>`GL_CONNECTORS_IDENTIFIER` (optional) |
| `main_with_native_tool.py` | `uv run python main_with_native_tool.py --all`<br>`uv run python main_with_native_tool.py --e2b`<br>`uv run python main_with_native_tool.py --serper`<br>`uv run python main_with_native_tool.py --browser`<br>`uv run python main_with_native_tool.py --query "..."` | Agent with native tools (E2B, Serper, Browser Use) | `OPENAI_API_KEY`<br>`E2B_API_KEY` (for `--e2b`)<br>`SERPER_API_KEY` (for `--serper`)<br>No API key needed for `--browser` |

## Running Examples with Command-Line Flags

### `main_with_native_tool.py` - Native Tools Testing

The `main_with_native_tool.py` example supports command-line flags to test specific native tools or run all tests:

```bash
# Run all tool tests sequentially (E2B, Serper, Browser)
uv run python main_with_native_tool.py --all

# Test individual tools
uv run python main_with_native_tool.py --e2b      # Test E2B code sandbox (generate chessboard)
uv run python main_with_native_tool.py --serper   # Test Google Serper web search
uv run python main_with_native_tool.py --browser  # Test Browser Use (find latest news in detik.com)

# Run with custom query
uv run python main_with_native_tool.py --query "Your custom query here"

# Default (no flags) - runs a simple web search test
uv run python main_with_native_tool.py
```

**Available Flags:**

- `--all`: Run all tool tests sequentially:
  - E2B Code Sandbox: Generate a chessboard using Python (8x8 grid)
  - Google Serper: Search for latest news about Barcelona football club
  - Browser Use: Navigate to detik.com and find latest news headlines

- `--e2b`: Test E2B code sandbox tool with chessboard generation

- `--serper`: Test Google Serper web search tool

- `--browser`: Test Browser Use tool to navigate and extract news from detik.com

- `--query <text>`: Run agent with a custom query

**Note**: See the "Required Env Vars" column in the examples table above for environment variable requirements. If `SERPER_API_KEY` is invalid or missing, the tool will return a 403 error but the agent handles it gracefully and provides a helpful fallback response.

## How It Works

Instead of the traditional pattern:

```python
# Server-backed execution (requires deploy)
agent = Agent(name="my-agent", instruction="...")
agent.deploy()  # Deploy to AIP server
result = agent.run("Hello")  # Runs on server
```

You can now simply:

```python
# Local execution (no deploy needed)
from langchain_core.tools import BaseTool

class MyTool(BaseTool):
    name = "my_tool"
    description = "Does something useful"

    def _run(self, query: str) -> str:
        return f"Result: {query}"

agent = Agent(
    name="my-agent",
    instruction="...",
    tools=[MyTool],  # Tools work locally!
)
result = agent.run("Hello")  # Runs locally with tools!
```

The `Agent.run()` method automatically detects:

1. If the agent has an ID (deployed) → uses server-backed execution
2. If no ID but `glaip-sdk[local]` is installed → uses local execution
3. Otherwise → raises an error with instructions

## Tool Support

### Supported in Local Mode

- LangChain `BaseTool` classes
- LangChain `BaseTool` instances
- `Tool.from_langchain()` wrappers
- Tools with `@tool_plugin` decorator (decorator is ignored locally)

### NOT Supported in Local Mode

- `Tool.from_native("tool_name")` - Requires platform
- String tool names - Require platform lookup

## Architecture

```
glaip-sdk                    aip-agents (local backend)
┌─────────────────┐         ┌─────────────────────┐
│  Agent.run()    │────────▶│  LangGraphReactAgent│
│                 │         │                     │
│  LangGraphRunner│────────▶│  arun_a2a_stream()  │
│                 │         │                     │
│  ToolAdapter    │────────▶│  tools=[BaseTool]   │
└─────────────────┘         └─────────────────────┘
```
