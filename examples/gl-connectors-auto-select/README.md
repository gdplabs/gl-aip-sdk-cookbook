# GL Connectors Auto-Select

Deploys an AIP agent that can **adjust its own capabilities in natural language**. Ask the
deployed agent things like *"give me the ability to create GitHub PRs"* or *"drop the Datadog
MCP"*, and it resolves the request against the GL Connectors catalog and attaches or detaches
the right **Tool**, **Skill**, or **MCP** on itself — no manual catalog browsing or SDK calls
on your part.

## How it works

`main.py` deploys a single agent via the [AIP Python SDK](https://pypi.org/project/glaip-sdk/)
(`glaip-sdk`) with three key pieces of configuration:

1. **The [`gl-connectors-picker`](https://github.com/GDP-ADMIN/prompt-template/tree/f/gl-connectors-skill/gdp-labs-wide/generic/skills/gl-connectors-picker)
   skill** is attached at deploy time. At runtime the skill parses the user's intent
   (add / remove / swap a capability), searches the GL Connectors catalog, selects the least
   bloated match by a **Tool → Skill → MCP** priority, confirms with the user, and then
   mutates the agent through the AIP API using read-modify-write so existing capabilities are
   preserved.

2. **A local-disk filesystem with `allow_execute=True`**, because the skill works by running
   its bundled scripts (`catalog_client.sh`, `agent_capability.py`) inside the agent's sandbox.

3. **Credentials injected into the filesystem `env`**, because the skill's scripts read them
   from the runtime environment:

   | Variable | Purpose |
   |----------|---------|
   | `AIP_API_URL` / `AIP_API_KEY` | Lets the agent call the AIP API to mutate agents (including itself). |
   | `GL_CONNECTORS_BASE_URL` / `GL_CONNECTORS_TOKEN` | Authenticates catalog search; the token is also wired into any tools/MCPs the skill attaches. |
   | `AIP_AGENT_NAME` | The agent's own name. Set automatically from `AGENT_NAME` — see limitation 3 below. |

The result is a self-referential loop: the deployed agent holds the credentials and identity
needed to call the AIP API **about itself**, so "give *me* the ability to X" works.

## Usage

1. Create a `.env` file (it is git-ignored) with the four required credentials, and
   optionally an agent name:

   ```dotenv
   AIP_API_URL=...
   AIP_API_KEY=...
   GL_CONNECTORS_BASE_URL=...
   GL_CONNECTORS_TOKEN=...
   # optional, defaults to glconnectors-auto-select-tester-unique
   AGENT_NAME=my-self-modifying-agent
   ```

2. Deploy:

   ```sh
   uv run main.py
   ```

3. Talk to the deployed agent on AIP and ask it to add, remove, or swap capabilities.

## Limitations / points of improvement

1. **All credentials must be injected at agent creation.** All four secrets
   (`AIP_API_URL`, `AIP_API_KEY`, `GL_CONNECTORS_BASE_URL`, `GL_CONNECTORS_TOKEN`) have to be
   supplied by the user and baked into the agent's filesystem `env` at deploy time, where they
   persist in the agent's config. Ideally AIP could infer or broker these credentials itself
   (e.g. platform-managed identity or secret references), or at minimum offer better
   credential-handling primitives than plain env injection.

2. **The AIP CLI can't be used for this yet.** At the time of writing, deploying with skills,
   a filesystem config, etc. is not yet possible through the AIP CLI, so this example must go
   through the Python SDK.

3. **AIP cannot infer the current agent's name.** A running agent has no runtime signal for
   its own identity, so we must feed it in ourselves — either via the `AIP_AGENT_NAME` env var
   (as done here) or by hard-coding it into the agent instruction. Native self-identity in AIP
   would be a huge boon for this skill's self-referential use case, letting any agent improve
   itself without deploy-time wiring.
