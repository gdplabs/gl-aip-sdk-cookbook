# Multi-Agent System Patterns

This directory contains examples demonstrating various multi-agent system patterns using the GLAIP SDK.

Note: Commands below assume you run them from this folder unless noted otherwise.

## Available Patterns

- **Aggregator**: Agents contribute outputs that are collected and synthesized by an aggregator agent
- **Hierarchical**: Agents organized in a hierarchical structure with parent-child relationships
- **Loop**: Agents that iterate and refine outputs through multiple passes
- **Parallel**: Multiple agents execute simultaneously on different tasks
- **Router**: A central router determines which agent(s) to invoke based on the task
- **Sequential**: Tasks processed sequentially where one agent's output becomes the next agent's input

Each pattern includes a detailed README with examples and documentation. Navigate to the individual pattern directories for more information.

## Prerequisites

- This example set runs locally (no `agent.deploy()`), so `AIP_API_KEY` / `AIP_API_URL` are not required.
- Install dependencies with `uv sync`.
- Set `OPENAI_API_KEY` (or configure another supported LLM provider in your environment).

## Quick Start

```bash
uv sync
uv run <pattern-name>/main.py
```

Replace `<pattern-name>` with one of: `aggregator`, `hierarchical`, `loop`, `parallel`, `router`, or `sequential`.
