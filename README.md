# 🍧 GL AIP (GDP Labs AI Agent Package) Cookbook

Welcome to the **GL AIP Cookbook** - a comprehensive collection of sample code and examples for working with the GL AIP SDK.

## Quick Start

1. Install Python 3.11 or 3.12
2. Install [uv](https://docs.astral.sh/uv/)
3. Pick an example under [`./examples`](./examples/) and follow that example's README

## Examples

- **Default server-backed flows**: `hello-world`, `multi-agent`, `runtime-config`, `modular-tool-integration`, `agent-export-import`
- **Local-run flows**: `hello-world-local`, `multi-agent-system-patterns`, `tool-state-handoff-local`

Each example README contains its own prerequisites and environment configuration.

## Agent Skills Quick Guidance

Use Agent Skills when:

- You have repeated instruction blocks across agents or workflows.
- You need one reusable policy/contract shared in multiple places.
- You want cleaner top-level prompts (orchestrator style).

Avoid Agent Skills when:

- The task is tiny and the base prompt is already short.
- You plan to put too much logic into one giant skill file.
- You do not have a benchmark to verify token/latency impact.

Possible side effects (if overused or overloaded):

- Higher input tokens (skill references + large skill content overhead).
- Slower runtime from extra context handling.
- Harder debugging when logic is spread across too many skills.

Recommendation:

- Always benchmark baseline vs skills on the same scenario before rollout.
- Keep skills focused and modular; avoid mega-skills.
- Provide both local and remote examples when documenting a skills flow.

Explore the subdirectories in the [examples](./examples/) folder for hands-on code and setup instructions.
