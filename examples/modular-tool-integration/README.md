# Modular Tool Integration (Travel Assistant)

This example demonstrates how to build a complex agent that uses multiple tools organized across separate files and packages.

Note: Commands below assume you run them from this folder unless noted otherwise.

Default run mode in this example is deployment (`agent.deploy()`). If you keep deployment mode, set `AIP_API_URL` and `AIP_API_KEY`.

## Key Features
- **Modular Packaging**: The Weather tool is a full Python package (`weather/`) with internal helper files.
- **Standalone Tools**: Flight status, Stock checker, and Travel math tools are simple single-file implementations.
- **Agent Orchestration**: A single agent intelligently selects between these specialized tools.

## Structure
- `main.py`: The orchestration script.
- `tools/weather/`: A modular tool package with helper logic.
- `tools/flight_status.py`: Single-file tool example.
- `tools/stock_checker.py`: Single-file tool example.
- `tools/travel_math.py`: Single-file tool example.

## ⚙️ Prerequisites

- Python 3.11 or 3.12
- `uv` package manager
- Server-backed execution credentials:
  - `AIP_API_KEY`
  - `AIP_API_URL`

## 🚀 Getting Started

Optional (skip if you are already in `gl-aip/examples/modular-tool-integration`):

```bash
git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/gl-aip/examples/modular-tool-integration
```

### 1. Install Dependencies

```bash
uv sync
```

This command installs the GLAIP-SDK and other dependencies as specified in `pyproject.toml`.

For detailed GLAIP SDK installation instructions, see the [official installation guide](https://gdplabs.gitbook.io/gl-aip/gl-aip-sdk/get-started/install-and-configure).

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your AIP_API_KEY and AIP_API_URL
```

### 3. Run the Example

```bash
uv run main.py
```
