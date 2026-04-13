# Filesystem Middleware Cookbook

Runnable scenarios for the Agent Filesystem — beyond the GitBook reference.

Each example demonstrates a **workflow pattern** the docs describe but don't show end-to-end, using `aip_agents` directly for local execution.

## Prerequisites

- Python 3.11 or 3.12
- [uv](https://docs.astral.sh/uv/)
- `OPENAI_API_KEY` — required for all examples
- `E2B_API_KEY` — required only for `07_sandbox_execute.py`

## Quick Start

```bash
cd examples/filesystem-middleware
cp .env.example .env   # Add your API keys
uv sync
uv run python 01_file_discovery.py
```

## Examples

| # | File | Scenario | Key Pattern | Requires |
|---|------|----------|-------------|----------|
| 01 | `01_file_discovery.py` | Discover and read files | ls → read_file | OPENAI_API_KEY |
| 02 | `02_file_lifecycle.py` | Create then modify a file | write_file → edit_file | OPENAI_API_KEY |
| 03 | `03_data_pipeline.py` | CSV to report pipeline | read → aggregate → write | OPENAI_API_KEY |
| 04 | `04_codebase_analysis.py` | Search across 15+ files | grep → read_file → report | OPENAI_API_KEY |
| 05 | `05_security_audit.py` | Find hardcoded secrets | grep → read_file → risk report | OPENAI_API_KEY |
| 06 | `06_tool_output_eviction.py` | Large output → auto-save → read back | custom tool + eviction config | OPENAI_API_KEY |
| 07 | `07_sandbox_execute.py` | Run Python in isolated sandbox | execute + artifact tracking | E2B_API_KEY |

## GitBook Reference

- [Agent Filesystem Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agent-filesystem) — tool reference, backend options, pagination
- [Sandbox Deep Dive](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agent-filesystem/sandbox) — sandbox setup and configuration
- [File Processing Guide](https://gdplabs.gitbitbook.io/sdk/gl-ai-agent-package/guides/file-processing) — document ingestion (attachments/chunks)