# Parallel Pattern

Multiple agents work simultaneously on different parts of a task.

Note: Commands below assume you run them from this folder unless noted otherwise.

## Demo Scenario: Trip Planning with Specialized Agents

This minimal example shows two agents working simultaneously on different tasks. The system includes:

- **Logistics Agent**: Focuses ONLY on travel logistics like flights, hotels, transport
- **Activities Agent**: Focuses ONLY on things to do, attractions, food

Both agents work in parallel on the query "Plan a 5-day trip to Tokyo", with each
agent providing their specialized expertise simultaneously. The results are then
presented separately, showing how parallel processing can handle different aspects
of a complex task concurrently.

This pattern is ideal when you have independent subtasks that can be processed simultaneously to reduce overall processing time.

## Quick Start

```bash
uv run main.py
```

## Documentation

See the [Parallel Pattern](https://glaip-sdk.gitbook.io/docs/how-to-guides/multi-agent-system-patterns/parallel) guide for full documentation.
