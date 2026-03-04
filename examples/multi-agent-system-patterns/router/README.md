# Router Pattern

A central router determines which agent(s) to invoke based on the task or input.

Note: Commands below assume you run them from this folder unless noted otherwise.

## Demo Scenario: Language Translation Router

This example demonstrates a router pattern with language translation queries. The system includes:

- **Router Agent**: Analyzes the user's query and determines which language expert to route to
- **Spanish Expert**: Handles Spanish language queries, translations to/from Spanish
- **Japanese Expert**: Handles Japanese language queries, translations to/from Japanese

The router processes queries like:

- "How do you say 'love' in Spanish?" → Routes to Spanish Expert
- "What is the meaning of 'arigatou' in English?" → Routes to Japanese Expert
- "How do you say 'hello' in German?" → Responds that no expert is available

This pattern is useful when you have multiple specialized agents and need intelligent routing based on the input characteristics or content.

## Quick Start

```bash
uv run main.py
```

## Documentation

See the [Router Pattern](https://glaip-sdk.gitbook.io/docs/how-to-guides/multi-agent-system-patterns/router) guide for full documentation.
