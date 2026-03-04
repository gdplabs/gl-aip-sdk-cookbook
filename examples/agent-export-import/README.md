## ⚙️ Prerequisites

Note: Commands below assume you run them from this folder unless noted otherwise.

- Python 3.11 or 3.12
- `uv` package manager
- Server-backed execution credentials:
  - `AIP_API_KEY`
  - `AIP_API_URL`

## 🚀 Getting Started

Optional (skip if you are already in `gl-aip/examples/agent-export-import`):

```bash
git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
cd gen-ai-sdk-cookbook/gl-aip/examples/agent-export-import
```

### 1. Install Dependencies

```bash
uv sync
```

This command installs the GLAIP-SDK as specified in `pyproject.toml`.

For detailed GLAIP SDK installation instructions, see the [official installation guide](https://gdplabs.gitbook.io/gl-aip/gl-aip-sdk/get-started/install-and-configure).

### 2. Run the Example

```bash
uv run main.py
```

## 📖 What This Example Demonstrates

This cookbook demonstrates GLAIP's powerful **agent export/import mechanism**, which allows you to:

1. **Export agent configurations** to JSON or YAML files for:
   - Version control and backup
   - Sharing agent templates across teams
   - Cloning agents with modifications
   - Documentation and auditing

2. **Import agent configurations** to:
   - Recreate agents from templates
   - Clone existing agents with customizations
   - Migrate agents between environments
   - Restore from backups

## 🎯 Key Features

### Export Formats
- **JSON**: Machine-readable, ideal for programmatic processing
- **YAML**: Human-readable, great for documentation and manual editing

### Export Contents
The export includes comprehensive agent configuration:
- Name, instruction, and model settings
- Tool attachments (with full tool details)
- Sub-agent relationships (with full agent details)
- Timeout and execution settings
- Metadata and custom configurations

### Import Flexibility
- **CLI Override**: Command-line arguments override imported values
- **Merge Strategy**: Tools and agents can be combined from both sources
- **Format Auto-detection**: Automatically detects JSON or YAML from file extension

## 💡 Use Cases

1. **Agent Templates**: Create reusable agent configurations
2. **Environment Migration**: Move agents from dev to production
3. **Team Collaboration**: Share agent configurations via version control
4. **Backup & Recovery**: Save and restore agent configurations
5. **Agent Cloning**: Create variations of existing agents

## 📋 Expected Output

Upon successful execution, you should see:

```
═══════════════════════════════════════════════════════════════════════════════
                    Agent Export/Import Mechanism Demo
═══════════════════════════════════════════════════════════════════════════════

Step 1: Creating Original Agent
────────────────────────────────────────────────────────────────────────────────
✅ Created agent: customer-support-agent (ID: abc-123-def)

Step 2: Exporting Agent to JSON
────────────────────────────────────────────────────────────────────────────────
✅ Exported to: customer-support-agent.json

Step 3: Exporting Agent to YAML
────────────────────────────────────────────────────────────────────────────────
✅ Exported to: customer-support-agent.yaml

Step 4: Importing and Creating New Agent from JSON
────────────────────────────────────────────────────────────────────────────────
✅ Created cloned agent: customer-support-agent-clone (ID: xyz-456-ghi)

Step 5: Importing with CLI Overrides
────────────────────────────────────────────────────────────────────────────────
✅ Created customized agent: premium-support-agent (ID: jkl-789-mno)

Step 6: Testing Cloned Agent
────────────────────────────────────────────────────────────────────────────────
🤖 Running: "What are your business hours?"

───────────────────────────────── Final Result ─────────────────────────────────
Our business hours are Monday through Friday, 9 AM to 5 PM EST. For urgent 
matters outside these hours, please use our emergency contact form.
────────────────────────────────────────────────────────────────────────────────

✅ Cleanup Complete
All test agents deleted successfully.
```

## 🔧 CLI Usage Examples

### Export Agent Configuration

```bash
# Export to JSON (default)
aip agents get my-agent --export agent.json

# Export to YAML (human-readable)
aip agents get my-agent --export agent.yaml

# Export with full details
aip agents get customer-support --export backup.json
```

### Import Agent Configuration

```bash
# Create agent from JSON file
aip agents create --import agent.json

# Create agent from YAML file
aip agents create --import agent.yaml

# Import with CLI overrides (CLI args take precedence)
aip agents create --import agent.json --name "new-agent-name"

# Import and add additional tools
aip agents create --import agent.json --tools additional-tool-id
```

### Update Existing Agent from Import

```bash
# Update agent from exported configuration
aip agents update agent-id --import updated-config.json

# Update with selective overrides
aip agents update agent-id --import config.yaml --instruction "New instruction"
```

## 📄 Export File Examples

### JSON Format (`agent.json`)

```json
{
  "name": "customer-support-agent",
  "instruction": "You are a helpful customer support agent...",
  "model": "gpt-4.1",
  "timeout": 300,
  "tools": [
    {
      "id": "tool-123",
      "name": "knowledge_base_search",
      "description": "Search company knowledge base"
    }
  ],
  "agents": [],
  "metadata": {
    "version": "1.0",
    "department": "support"
  }
}
```

### YAML Format (`agent.yaml`)

```yaml
name: customer-support-agent
instruction: |
  You are a helpful customer support agent.
  
  Your responsibilities:
  - Answer customer questions
  - Search the knowledge base
  - Escalate complex issues
model: gpt-4.1
timeout: 300
tools:
  - id: tool-123
    name: knowledge_base_search
    description: Search company knowledge base
agents: []
metadata:
  version: '1.0'
  department: support
```

## 🎓 Advanced Patterns

### 1. Agent Template Library

Create a library of reusable agent templates:

```bash
# Export templates
aip agents get research-agent --export templates/research.yaml
aip agents get writer-agent --export templates/writer.yaml
aip agents get reviewer-agent --export templates/reviewer.yaml

# Use templates to create new agents
aip agents create --import templates/research.yaml --name "market-research"
aip agents create --import templates/writer.yaml --name "blog-writer"
```

### 2. Environment Migration

Move agents between development and production:

```bash
# Export from development
export AIP_API_URL="https://dev.example.com/api"
aip agents get dev-agent --export agent-config.json

# Import to production
export AIP_API_URL="https://prod.example.com/api"
aip agents create --import agent-config.json --name "prod-agent"
```

### 3. Agent Versioning

Maintain version history of agent configurations:

```bash
# Export with version in filename
aip agents get my-agent --export my-agent-v1.0.json

# Make changes and export new version
aip agents update my-agent --instruction "Updated instruction"
aip agents get my-agent --export my-agent-v1.1.json

# Rollback if needed
aip agents update my-agent --import my-agent-v1.0.json
```

### 4. Batch Agent Creation

Create multiple agents from templates:

```python
from glaip_sdk import Client
from pathlib import Path
import json

client = Client()
template_dir = Path("templates")

# Create agents from all templates
for template_file in template_dir.glob("*.json"):
    with open(template_file) as f:
        config = json.load(f)
    
    agent = client.create_agent(**config)
    print(f"Created: {agent.name} (ID: {agent.id})")
```

## 🔍 Troubleshooting

### Common Issues

**Issue: "PyYAML is required for YAML export"**
```bash
# Solution: Install PyYAML
pip install PyYAML
# or with uv
uv pip install PyYAML
```

**Issue: "Tool not found" during import**
```bash
# Solution: Ensure tools exist before importing
aip tools list  # Check available tools
# Create missing tools or update the import file with correct tool IDs
```

**Issue: "Multiple agents named 'X'" during import**
```bash
# Solution: Use agent IDs instead of names in the import file
# Or ensure unique naming
```

## 🎯 Best Practices

1. **Use YAML for Human Editing**: YAML is more readable and easier to edit manually
2. **Use JSON for Automation**: JSON is better for programmatic processing
3. **Version Control**: Store exported configurations in Git for history tracking
4. **Naming Convention**: Use descriptive names with versions (e.g., `agent-v1.0.json`)
5. **Validate Before Import**: Review exported files before importing to new environments
6. **Backup Regularly**: Export critical agents regularly for disaster recovery
7. **Document Changes**: Add comments in YAML files to explain configuration choices

## 📚 Related Resources

- [GLAIP SDK Documentation](https://gdplabs.gitbook.io/gl-aip/gl-aip-sdk)
- [Agent Management Guide](https://gdplabs.gitbook.io/gl-aip/gl-aip-sdk/guides/agents)
- [CLI Reference](https://gdplabs.gitbook.io/gl-aip/gl-aip-sdk/cli-reference)

## 🤝 Contributing

Found an issue or have suggestions? Please open an issue or submit a pull request!
