# Google Calendar Connector Examples

---

## Overview

This folder contains example scripts demonstrating the Google Calendar connector with the GL Connectors SDK.

---

## Prerequisites

- Python 3.12
- A reachable GL Connectors server and a `GL_CONNECTORS_USER_TOKEN`
- `OPENAI_API_KEY` — required OpenAI API key (examples require this to run)

---

## Environment (.env)

1. Copy the example env file to create a local `.env`:

   - Windows (PowerShell):

    ```
     copy .env.example .env
    ```

   - macOS / Linux:
  
    ```
    cp .env.example .env
    ```

2. Edit `.env` and fill the values. Keys required (see `.env.example`):

- `GL_CONNECTORS_URL` — the connector server URL
- `GL_CONNECTORS_USER_TOKEN` — token for authenticating connector requests
- `OPENAI_API_KEY` — OpenAI API key

---

## Install dependencies

Run `uv sync` from inside the `google_calendar` folder to install the project's dependencies (reads `pyproject.toml`):

```bash
# from the google_calendar folder
uv sync
```

If you don't have `uv` installed, install it first with:

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Notes:

- `uv sync` will use `uv.lock` if present to ensure reproducible installs.
- If you delete `.venv` and `uv.lock` and then run `uv sync`, `uv` will recreate them when it is managing environments.

---

## Run the examples

After filling `.env` and installing dependencies you can run the example scripts. Run them using `uv run` after activating the `.venv`.

Examples using `uv`:

Run these `uv` commands from inside the `google_calendar`  folder.

```bash
uv run examples_get_event.py
uv run examples_insert_event.py
uv run examples_update_event.py
uv run examples_delete_event.py
```

---

## Troubleshooting

- If authentication fails, verify `GL_CONNECTORS_URL`, `GL_CONNECTORS_USER_TOKEN`, and `OPENAI_API_KEY` values in your `.env`.
- Ensure your Python interpreter is version 3.12 when running the examples.
- Verify network/firewall settings allow outgoing requests to `GL_CONNECTORS_URL`.

---
