## ⚙️ Prerequisites

Refer to the [main prerequisites documentation](../../README.md#️-prerequisites) for detailed setup requirements.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/gl-aip/examples/langflow-execute-agents
```

### 2. Install Dependencies

```bash
uv sync
```

This command installs the GL AIP as specified in `pyproject.toml`.

For detailed GL AIP installation instructions, see the [official installation guide](https://gdplabs.gitbook.io/gl-aip/gl-aip-sdk/get-started/install-and-configure).

### 3. Configure Environment Variables

Before running the example, set the required environment variables:

```bash
export AIP_API_URL="https://demo-aip.obrol.id/"
export AIP_API_KEY="your-api-key-here"
```

> **Note:** Replace `your-api-key-here` with your actual AIP API key.

### 4. Run the Examples

This cookbook provides three ways to interact with Langflow agents:

**Option 1: Interactive (Recommended for first-time users)**

```bash
uv run main.py
```

This interactive script will:
1. List all available agents
2. Prompt you to enter an agent ID
3. Ask for your prompt
4. Run the agent and display results


> Option 2 and 3 is recommended for advanced users who want to run agents programmatically and it has less code.

**Option 2: List agents separately**

```bash
uv run list_agents.py
```

**Option 3: Run a specific agent**

```bash
uv run run_agent.py
```

> **Note:** Before running `run_agent.py`, edit the file to set your `agent_id` and `prompt`.

## 📖 What This Example Demonstrates

This example shows how to work with Langflow agents using the GL AIP SDK:

### `main.py` (Interactive)
- **All-in-one interactive experience**
- Lists all available agents with their IDs and names
- Prompts user to input agent ID and custom prompt
- Retrieves agent configuration and executes the agent
- Displays the formatted response

### `list_agents.py` (Standalone)
- Sync Langflow agents from AIP
- Lists all available **Langflow** agents in your AIP instance
- Displays agent ID and name for each agent
- Useful for discovering available Langflow agents

### `run_agent.py` (Standalone)
- Retrieves and displays agent configuration by ID
- Executes a Langflow agent with a custom prompt
- Shows the agent's response to your query

## 📋 Expected Output

### Running `main.py` (Interactive)

The interactive script will guide you through the process:

```
================================================================================
Available Agents:
================================================================================
0d0bxxxx2cab4 Langflow_Interview_Availability_Checker
ee43xxxxd0620 CatFactAgent
ae0exxxx61d5a weather_forecast_agent
[... more agents ...]
================================================================================

Enter the Agent ID you want to use: 0d0bxxxx2cab4

✓ Agent found: Langflow_Interview_Availability_Checker

================================================================================
Enter your prompt:
================================================================================
(Type your prompt and press Enter)
I have a meeting at 13.30 until 14.00 Jakarta Time Zone, Check my availability to attend an interview today at 13.00 until 21.00 Jakarta Time Zone

================================================================================
Running Agent...
================================================================================

[Agent response with formatted output]
```

### Running `list_agents.py`

This will display all available agents:

```
0d0bxxxx2cab4 Langflow_Interview_Availability_Checker
ee43xxxxd0620 CatFactAgent
ae0exxxx61d5a weather_forecast_agent
[... more agents ...]
```

### Running `run_agent.py`

After setting your `agent_id` and `prompt`, you will see:

```
{'langflow': {'api_key': 'sk-...', 'flow_id': '36ea89c3-...', 'base_url': 'https://langflow.obrol.id'}, 
 'lm_provider': 'openai', 'lm_name': 'gpt-4o-mini', 'lm_hyperparameters': {'temperature': 0.0}, ...}

─────────────────────────── 🤖 0d0bxxxx2cab4 ───────────────────────────
 ──────────────────────────────────── User Request ────────────────────────────────────
  Query: I have a meeting at 13.30 until 14.00 Jakarta Time Zone, Check my availability 
  to attend an interview today at 13.00 until 21.00 Jakarta Time Zone
 ───────────────────────────────────────────────────────────────────────────────────────
 ──────────────────────────────────────── Steps ────────────────────────────────────────
  No steps yet
 ───────────────────────────────────────────────────────────────────────────────────────
 ────────────────────────────────── Final Result · 2.47s ───────────────────────────────
  You have a meeting scheduled from 13:30 to 14:00 Jakarta Time. Therefore, you will 
  not be available for an interview during that time.

  Your availability for the interview today is as follows:
  • 13:00 to 13:30: Available
  • 14:00 to 21:00: Available

  You can attend an interview before your meeting or after it.
 ───────────────────────────────────────────────────────────────────────────────────────
```

## 💡 Use Cases

- **Agent Discovery**: Use `list_agents.py` to discover all Langflow agents available in your AIP instance
- **Agent Configuration**: View detailed configuration (model, instruction, Langflow settings) of specific agents
- **Programmatic Execution**: Execute Langflow agents via SDK with custom prompts using `run_agent.py`
- **Automation**: Integrate Langflow agents into your workflows and applications
- **Interview Scheduling**: Example use case with the Interview Availability Checker agent

## 📚 Reference

- [GL AIP SDK Documentation](https://gdplabs.gitbook.io/gl-aip/gl-aip-sdk)
- [Langflow Integration Guide](https://gdplabs.gitbook.io/gl-aip/how-to-guides/langflow-integration-guide)
- [Agent Management Guide](https://gdplabs.gitbook.io/gl-aip/how-to-guides/agents-guide)