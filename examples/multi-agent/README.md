# Hello World - Multi-Agent

An example demonstrating the multi-agent coordinator pattern with sub-agents and shared tools.

Note: Commands below assume you run them from this folder unless noted otherwise.

**Pattern:** Multi-agent with coordinator
**Use when:** Complex workflows requiring multiple specialized agents

Default run mode in this example is deployment (`agent.deploy()`). If you keep deployment mode, set `AIP_API_URL` and `AIP_API_KEY`.

## Architecture

```
GreetingCoordinator (coordinator)
├── FormalGreeter (sub-agent) - formal greetings
├── CasualGreeter (sub-agent) - casual greetings
└── Shared GreetingTool (deployed only once)
```

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

## Project Structure

```
hello-world-multi-agent/
├── agents/
│   ├── greeting_coordinator.py  # Coordinator agent
│   ├── formal_greeter.py        # Sub-agent
│   └── casual_greeter.py        # Sub-agent
├── tools/
│   ├── greeting.py              # Shared custom tool
│   └── farewell.py              # Additional tool
├── main.py                      # Entry point
├── pyproject.toml
└── .env.example
```
