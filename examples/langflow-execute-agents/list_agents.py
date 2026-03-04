from glaip_sdk import Client

client = Client()

client.sync_langflow_agents()

# the `agent_type="langflow"` is optional, it will only list agents that are created using Langflow
for agent in client.agents.list_agents(agent_type="langflow"):
    print(agent.id, agent.name)
