from glaip_sdk import Client

client = Client()

# get your agent_id from list_agents.py
agent_id = "your-agent-id-here"

agent = client.agents.get_agent_by_id(agent_id)
print("Agent Name: {}".format(agent.name))

# create your prompt here
prompt = "your-prompt-here"
response = client.agents.run_agent(agent_id, prompt)
print(response)
