# Loop Pattern

Agents operate in iterative cycles, continuously improving their outputs based on feedback from other agent(s).

Note: Commands below assume you run them from this folder unless noted otherwise.

## Demo Scenario: Code Optimization Loop

This example demonstrates an autonomous internal loop via sub-agent delegation. The system includes:

- **Optimizer Agent**: Proposes code improvements and manages the optimization process
- **Executor Agent**: Runs and benchmarks the proposed code, measuring runtime and correctness

The optimizer performs up to 3 iterations: it proposes code, delegates to the executor to run and benchmark it, reads the report, refines if needed, then stops.

In the demo, the goal is to produce a minimal, correct Python program that counts
total prime numbers up to 10^6 with the expected output of 78498 and runtime less
than 1 second. The system starts from a basic approach and optimizes iteratively
until the requirements are met.

## Quick Start

```bash
uv run main.py
```

## Documentation

See the [Loop Pattern](https://glaip-sdk.gitbook.io/docs/how-to-guides/multi-agent-system-patterns/loop) guide for full documentation.
