# Tool State Handoff (Local)

**Warning**
This is a PoC, future version should use write file and read file interface from AIP

This example uses a toy verification scenario so the handoff is easy to confirm from the final model response.

- tool 1 shows the model some visible case notes
- tool 1 also stores a hidden verification code in agent `metadata`
- tool 2 receives only a short model summary, reads the stored metadata, and reveals the hidden code

If the final answer contains the hidden code, the second tool successfully read the metadata handoff.

It was tested with the local dependencies installed for this example from `pyproject.toml`.
If the SDK/runtime changes, re-check how metadata is propagated into tools.

## Pattern

1. `load_case_file` returns visible notes in its normal tool `result`, so the model can read them.
2. The same tool stores both those notes and a hidden verification code in `Command(update={"metadata": ...})`.
3. The model reads the visible notes and produces only a short `summary`.
4. `reveal_verification_code` receives only that `summary`, then reads the earlier handoff payload from `config["metadata"]` via `RunnableConfig`.

The important split is:

- `result` is for the model to read
- `metadata` is for the next custom tool to reuse

That lets the model see the first tool output without copying the whole payload into the second tool call.

## Why This Scenario Is Easy To Verify

The hidden verification code is not shown in tool 1's visible output.
So the model cannot know it on its own.

If tool 2 reveals a code such as `ALPHA-42` in its output, that code came from the metadata handoff.
That makes the success condition easy to inspect from the final response.

## What This Example Uses From Agent State

As of this stack, the state-derived handoff shown here is `metadata` mirrored into `RunnableConfig`.
In this example, the working read path is `config["metadata"]`.

The concrete payload shape used here is:

```python
config["metadata"]["handoff_state"] = {
    "case_name": "checkout_delay",
    "public_notes": [...],
    "hidden_verification_code": "ALPHA-42",
}
```

Tool 1 needs to return a `Command` because it stores data into agent `metadata`.
Tool 2 reads from `config["metadata"]`, and in this version it also returns a `Command` to scrub the handoff state after reading it.

That second `Command` is not required for reading.
It is only there to reduce repeated exposure of the hidden value in later events.

## Why `metadata`

This example uses `metadata` because the handoff payload is small and short-lived:

- case name
- visible notes
- hidden verification code

Use this pattern for small structured data needed by the next tool call.
Do not treat this as a place for large documents, binary payloads, or durable workflow state.

## Precondition

`reveal_verification_code` is intended to run after `load_case_file`, because it reads
`metadata.handoff_state` when present.

In this demo, `main.py` instructs the model to call `load_case_file` first, but that is guidance rather than a hard runtime guarantee.
If the metadata is missing, the tool returns `MISSING-CODE`, which means the intended handoff did not happen.

## Cleanup After Read

The current event stream includes metadata snapshots in tool events.
Because of that, any hidden value stored in metadata can appear in the stream more than once if it remains in state.

To reduce that repetition, `reveal_verification_code` rewrites `handoff_state` after reading it and removes the hidden code from metadata.
This does not prevent the first exposure after tool 1 writes the metadata, but it avoids carrying the hidden value forward in later state snapshots.

## Why The Second Tool Uses `RunnableConfig`

`reveal_verification_code` reads from `RunnableConfig` because that is the cleanest working read surface in this stack.

- tool 1 writes `metadata`
- the runtime mirrors that metadata into the next tool's config
- tool 2 reads the mirrored value from `config["metadata"]`

## Files

- `main.py`: local `Agent(...)` setup
- `tools/load_case_file.py`: tool 1 returns visible notes and stores hidden metadata in `handoff_state`
- `tools/reveal_verification_code.py`: tool 2 reads `config["metadata"]` and reveals the hidden code
- `.python-version`: pinned to Python `3.12`
- `pyproject.toml`: uv project config

## Quick Start

1. Create env file

   ```bash
   cp .env.example .env
   # Fill in OPENAI_API_KEY
   ```

2. Install dependencies

   ```bash
   uv sync
   ```

3. Run the PoC

   ```bash
   uv run python main.py
   ```

## What To Look For In The Run

- `load_case_file` returns visible notes for the model
- `load_case_file` also writes `metadata.handoff_state`
- the model calls `reveal_verification_code` with only `summary`
- `reveal_verification_code` returns the hidden verification code from `config["metadata"]`
