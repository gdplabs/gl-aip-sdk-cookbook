# Aggregator Pattern

Agents contribute outputs that are collected and synthesized by an aggregator agent into a final result.

Note: Commands below assume you run them from this folder unless noted otherwise.

## Demo Scenario: Daily Briefing Synthesizer

This example demonstrates an aggregator agent that synthesizes outputs from multiple
specialized sub-agents (time/calendar, weather, news), each with a mock tool returning
static values. The aggregator combines the information from these agents to create a
cohesive daily briefing for the user.

The system includes:

- **Time/Calendar Agent**: Provides current time and calendar events
- **Weather Agent**: Provides weather forecast information
- **Aggregator Agent**: Synthesizes all inputs into a concise morning briefing

This pattern is useful when you need to collect information from multiple sources and present it in a unified, well-formatted output.

## Quick Start

```bash
uv run main.py
```

## Documentation

See the [Aggregator Pattern](https://glaip-sdk.gitbook.io/docs/how-to-guides/multi-agent-system-patterns/aggregator) guide for full documentation.
