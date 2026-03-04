"""Agent Export/Import Mechanism Demo

Demonstrates GLAIP's agent export/import capabilities:
- Export agents to JSON formats
- Import agents from configuration files
"""

import json
from pathlib import Path

from glaip_sdk import Client

client = Client()

# Create original agent
original_agent = client.create_agent(
    name="customer-support-agent",
    instruction="""You are a helpful customer support agent.
Answer questions about products, provide troubleshooting help, and share business hours.
Business hours: Monday-Friday, 9 AM - 5 PM EST""",
    model="gpt-4.1",
)

# Export to JSON
json_file = Path("customer-support-agent.json")
export_data = {
    "name": original_agent.name,
    "instruction": original_agent.instruction,
    "model": "gpt-4.1",
}

with open(json_file, "w") as f:
    json.dump(export_data, f, indent=2)

print(f"Exported to: {json_file}")

# Import with modifications (also can import w.o. modification; a direct clone)
with open(json_file) as f:
    import_data = json.load(f)

import_data["name"] = "premium-support-agent"
import_data["instruction"] += "\n\nNote: Handle premium tier customers with priority support, use formal language."

premium_agent = client.create_agent(**import_data)
print(f"Created customized: {premium_agent.name}")

# Test cloned agent
result = premium_agent.run("What are your business hours?")
print(f"\nAgent response:\n{result}")

# Cleanup
original_agent.delete()
premium_agent.delete()
