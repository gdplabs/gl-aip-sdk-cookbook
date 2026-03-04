# Sequential Pattern

Tasks are processed sequentially, where one agent's output becomes the input for the next.

Note: Commands below assume you run them from this folder unless noted otherwise.

## Demo Scenario: Query Refinement and Answering

This example demonstrates a sequential workflow where one agent's output becomes the input for the next. The system includes:

- **Intent Refiner**: Takes a short or ambiguous user input and rewrites it as a clear, specific question
- **Coding Answerer**: Provides concise answers to coding questions, including minimal code snippets when appropriate

The workflow follows: User Input -> Intent Refiner -> Refined Question -> Coding Answerer -> Final Answer

In the demo, the input "python list to str" is first refined by the intent refiner into a clear question, then passed to the coding answerer who provides the solution with code examples.

## Quick Start

```bash
uv run main.py
```

## Documentation

See the [Sequential Pattern](https://glaip-sdk.gitbook.io/docs/how-to-guides/multi-agent-system-patterns/sequential) guide for full documentation.
