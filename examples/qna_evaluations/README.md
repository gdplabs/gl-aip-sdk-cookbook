# Comprehensive Agent Benchmark Evaluation System

Optimized, production-ready benchmark evaluation tool for GLAIP SDK agents with gllm-evals integration.

## Code Quality

This codebase follows strict quality guidelines:
- **DRY (Don't Repeat Yourself)**: Common patterns extracted into reusable methods
- **No Comments**: Clean, self-documenting code with descriptive names
- **Linting**: Proper Python style conventions
- **Modular**: Well-organized component structure

## Features

- ✅ Comprehensive data capture (trajectory, sources, steps, thinking)
- ✅ GLLM-Eval integration (completeness, groundedness, redundancy)
- ✅ Enhanced error handling with data capture on failures
- ✅ Concurrent and sequential execution modes (up to N parallel workers)
- ✅ Timeout debugging and performance tracking
- ✅ Optimized data size with essential fields only
- ✅ Native async support via `arun_agent` for better performance
- ✅ Clean, refactored codebase following best practices

## Installation

### 1. Setup: Makefile helper (project-local workflow)

This project provides a `Makefile` shortcut that wraps the Poetry installation and GCP auth configuration:

```bash
make install
```

This command:
- Configures Poetry HTTP basic credentials using your `gcloud auth print-access-token`
- Installs all dependencies (including `glaip-sdk`, `gllm-evals`, `ragas`, etc.) via `poetry install --all-extras`

You can choose either the manual `poetry install` flow below or the `make install` helper; both remain supported.

### 2a. Install Dependencies (Manual)

```bash
cd /path/to/benchmark
poetry install
```

### 2b. Install GLLM-Evals (Optional, for evaluation metrics)

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval]"
```

### 3. Default Configuration: .env-based configuration

Instead of exporting environment variables every time, you can place them in a local `.env` file (loaded automatically by `benchmark.py`).

```bash
cp .env.example .env
```

Then edit the file with your actual values:

```bash
# GLAIP Agent Configuration
AIP_API_URL=your_aip_api_url_here
AIP_API_KEY=your_aip_api_key_here

# OpenAI Configuration (for evaluation)
OPENAI_API_KEY=your_openai_api_key_here
```

When `.env` is present, `benchmark.py` will read these values on startup. You can still override them with `export` or CLI flags if needed.

## Usage

### Basic Usage

Assuming you have a `.env` file configured (see section 3 below):

```bash
# Run benchmark (no exports needed)
poetry run python benchmark.py \
  --input input.csv \
  --agent-id your-agent-id
```

If you prefer to export variables manually instead of using `.env`:

```bash
# Set environment variables
export AIP_API_URL=Your_AIP_API_URL
export AIP_API_KEY=your_api_key

# Run benchmark
poetry run python benchmark.py \
  --input input.csv \
  --agent-id your-agent-id \
  --openai-key your-openai-key
```

### Advanced Usage

```bash
# With all options
poetry run python benchmark.py \
  --input input.csv \
  --output results.csv \
  --agent-id 292bba97-55c1-4842-b133-d671606b29ff \
  --openai-key sk-... \
  --evaluation-model gpt-4o-mini \
  --limit 10 \
  --workers 5 \
  --use-arun \
  --agent-timeout 300
```

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | ✅ Yes | - | Input CSV file with questions |
| `--agent-id` | ✅ Yes | - | GLAIP Agent ID to evaluate |
| `--output` | No | Auto-generated | Output CSV file path |
| `--rows` / `-r` | No | - | Specific row numbers to process (e.g., `"1,3,5"`, `"1-5"`, or `"1,3-5,10"`) |
| `--openai-key` | No | `$OPENAI_API_KEY` | OpenAI API key for evaluation (can also be set via `.env`) |
| `--evaluation-model` | No | `gpt-4o-mini` | Model for GLLM-Eval |
| `--limit` | No | All rows | Limit number of questions |
| `--workers` | No | `1` | Number of parallel workers |
| `--use-arun` | No | `false` | Use arun_agent (native async) instead of run_agent |
| `--agent-timeout` | No | `300.0` | Agent timeout in seconds |

### Row selection with `--rows`

You can restrict the benchmark to specific rows from the input CSV without modifying the file:

```bash
# Run only rows 1, 3, and 5
poetry run python benchmark.py \
  --input input.csv \
  --agent-id your-agent-id \
  --rows "1,3,5"

# Run a range of rows
poetry run python benchmark.py \
  --input input.csv \
  --agent-id your-agent-id \
  --rows "10-20"

# Mix individual rows and ranges
poetry run python benchmark.py \
  --input input.csv \
  --agent-id your-agent-id \
  --rows "1,3-5,10"
```

The `--rows` flag is fully optional and co-exists with `--limit`; if both are provided, `--rows` determines the exact rows while `--limit` can still cap the total processed.

## Input CSV Format

Your input CSV must have a `Question` or `Questions` column. Optional columns:

| Column | Required | Description |
|--------|----------|-------------|
| `Question` / `Questions` | ✅ Yes | The question to ask the agent |
| `Expected Answer` | No | Expected answer for completeness evaluation |
| `Requires Visualization` | No | Flag for visualization requirements |

**Example CSV:**

```csv
Number,Question,Expected Answer,Requires Visualization
1,What are the two types of voyages?,Private Voyage and Shared Voyage,FALSE
2,What is the price of Ikan Kayu yacht?,USD 3500 per night,FALSE
```

## Output CSV Format

The output CSV includes comprehensive metrics:

### Core Fields
- `Index` - Question number
- `Question` - Original question
- `Expected Answer` - Expected answer (if provided)
- `Answer` - Agent's generated response
- `Response_Time` - Execution time in seconds

### Data Capture Fields
- `sources` - Formatted text of knowledge base chunks and tool outputs
- `retrieved_context` - JSON array of context items (for GLLM-Eval)
- `steps` - JSON array of tool execution steps
- `thinking_steps` - Agent's reasoning process

### Evaluation Metrics (GLLM-Eval)
- `geval_completeness` - Score 0-10: Does answer fully address question?
- `geval_groundedness` - Score 0-10: Is answer supported by context?
- `geval_redundancy` - Score 0-10: Is there unnecessary repetition?

### Error Fields
- `agent_error` - Error message if agent execution failed
- `evaluation_error` - Error message if evaluation failed
- `timeout_debug_info` - Debug info for timeout cases

## Execution Modes

### Concurrent Mode

```bash
# Process 5 questions in parallel
poetry run python benchmark.py \
  --input input.csv \
  --agent-id your-agent-id \
  --workers 5
```

**Use when:**
- Processing large datasets
- No rate limit concerns
- Faster execution needed

## Examples

### Example 1: Quick Test (1 question)

```bash
export AIP_API_URL=Your_AIP_API_URL
export AIP_API_KEY=your_key

poetry run python benchmark.py \
  --input input.csv \
  --agent-id 292bba97-55c1-4842-b133-d671606b29ff \
  --openai-key sk-... \
  --limit 1
```

### Example 2: Full Evaluation (10 questions, parallel)

```bash
poetry run python benchmark.py \
  --input input.csv \
  --agent-id 292bba97-55c1-4842-b133-d671606b29ff \
  --openai-key sk-... \
  --limit 10 \
  --workers 5
```

### Example 3: Without Evaluation (No OpenAI key)

```bash
# Still captures trajectory, sources, steps
poetry run python benchmark.py \
  --input input.csv \
  --agent-id 292bba97-55c1-4842-b133-d671606b29ff \
  --limit 10
```

## Understanding the Output

### Sources Field
Human-readable formatted text containing:
- Vector DB knowledge base chunks
- Tool execution outputs (SQL, API, etc.)
- References used in the final answer

**Format:**
```
[Reference 1] Title from source
Content of the reference...

[Tool: SQL Query Tool] SELECT * FROM...
Results: {...}
```

### Retrieved Context Field
JSON array of context items used by GLLM-Eval for groundedness:
- `final_response_reference` - Vector DB chunks
- `tool_panel_output` - Tool execution results

**Format:**
```json
[
  {
    "type": "final_response_reference",
    "content": "...",
    "title": "...",
    "source": "..."
  }
]
```

### Steps Field
JSON array of tool execution steps with timing:
```json
[
  {
    "tool_name": "hybrid_search",
    "duration_ms": 1234,
    "status": "success"
  }
]
```

## Troubleshooting

### Issue: "gllm-evals not found"

**Solution:** Install gllm-evals:
```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval]"
```

Or run without evaluation (no `--openai-key`).

### Issue: "Agent execution timed out"

**Solution:** Increase timeout:
```bash
--agent-timeout 600  # 10 minutes
```

### Issue: Empty retrieved_context for SQL agents

**Expected behavior:** SQL tool outputs are in `sources` field. The `retrieved_context` field only includes `final_response_reference` type (vector DB chunks) for evaluation.

### Issue: Rate limit errors

**Solution:** Reduce workers:
```bash
--workers 1  # Sequential execution
```

## Performance Tips

1. **Start small:** Test with `--limit 1` first
2. **Use concurrent mode:** Set `--workers 5` for faster processing
3. **Monitor timeouts:** Adjust `--agent-timeout` based on query complexity
4. **Check output regularly:** Verify data quality during long runs

## Output Analysis

### Analyzing Results with Python

```python
import pandas as pd
import json

# Load results
df = pd.read_csv('test_evaluation_optimized_20250108_123456.csv')

# Check completion rate
print(f"Successful: {df['agent_error'].isna().sum()}/{len(df)}")

# Average scores
print(f"Avg Completeness: {df['geval_completeness'].mean():.2f}")
print(f"Avg Groundedness: {df['geval_groundedness'].mean():.2f}")

# Check retrieved context
for idx, row in df.iterrows():
    if pd.notna(row['retrieved_context']):
        ctx = json.loads(row['retrieved_context'])
        print(f"Row {idx+1}: {len(ctx)} context items")
```

## Documentation

For detailed information, see:
- `GLLM_EVAL_EXPLANATION.md` - How GLLM-Eval uses the data
- `RETRIEVED_CONTEXT_VS_SOURCES_EXPLANATION.md` - Difference between fields
- `NO_FILTERING_SOLUTION.md` - Context filtering behavior

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review documentation files in this directory
3. Contact GDP Labs team