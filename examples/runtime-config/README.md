# Hello World - Runtime Config Demo

Demonstrates `runtime_config` for per-request overrides of agents, tools, and MCPs.

Note: Commands below assume you run them from this folder unless noted otherwise.

Default run mode in this example is deployment (`agent.deploy()`). If you keep deployment mode, set `AIP_API_URL` and `AIP_API_KEY`.

## Prerequisites

- Python 3.11 or 3.12
- `uv` package manager
- Server-backed execution credentials:
  - `AIP_API_KEY`
  - `AIP_API_URL`
- Optional for Arxiv MCP integration:
  - `ARXIV_MCP_API_KEY`
  - `ARXIV_MCP_AUTH_TOKEN`

## Setup

```bash
uv sync
```

Set required environment variables before running:

```bash
export AIP_API_KEY="your_api_key_here"
export AIP_API_URL="your_aip_api_url"
```

## Usage

### Deploy Agent

```bash
uv run python main.py
```

### Run Demo

```bash
uv run python demo_runtime_config.py
```

## runtime_config Examples

### 1. agent_config

Override agent behavior (planning, temperature, etc.):

```python
agent.run("query", runtime_config={
    "agent_config": {"planning": True}
})
```

### 2. tool_configs

Override tool configuration using SDK class or ID:

```python
agent.run("query", runtime_config={
    "tool_configs": {
        ResearchFormatterTool: {"style": "academic", "max_results": 3}
    }
})
```

### 3. mcp_configs

Override MCP authentication at runtime:

```python
agent.run("query", runtime_config={
    "mcp_configs": {
        arxiv_mcp: {
            "authentication": {
                "type": "custom-header",
                "headers": {"x-api-key": "new-key"}
            }
        }
    }
})
```

## Key Patterns

- **SDK objects as keys**: Use `ResearchFormatterTool` or `arxiv_mcp` directly
- **Strings as keys**: Use tool/MCP names or UUIDs
- **Conditional MCPs**: `arxiv_mcp` only created if env vars are set
