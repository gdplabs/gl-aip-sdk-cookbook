from glaip_sdk import Client

def main():
    client = Client()
    
    client.sync_langflow_agents()
    
    # List all available agents
    print("\n" + "="*80)
    print("Available Agents:")
    print("="*80)
    
    agents = list(client.agents.list_agents(agent_type="langflow"))
    
    if not agents:
        print("No Langflow agents found in your AIP instance.")
        return
    
    # Display agents
    for agent in agents:
        print("{} {}".format(agent.id, agent.name))
    
    print("="*80)
    
    # Get agent ID from user
    agent_id = input("\nEnter the Agent ID you want to use: ").strip()
    
    if not agent_id:
        print("No agent ID provided. Exiting...")
        return
    
    # Verify agent exists and get config
    try:
        agent = client.agents.get_agent_by_id(agent_id)
        print("\n✓ Agent found: {}".format(agent.name))
    except Exception as e:
        print("\n✗ Error: Could not find agent with ID '{}'")
        print(str(e))
        return
    
    # Get prompt from user
    print("\n" + "="*80)
    print("Enter your prompt:")
    print("="*80)
    print("(Type your prompt and press Enter)")
    
    prompt = input().strip()
    
    if not prompt:
        print("\nNo prompt provided. Exiting...")
        return
    
    # Run the agent
    print("\n" + "="*80)
    print("Running Agent...")
    print("="*80)
    
    try:
        client.agents.run_agent(agent_id, prompt)
    except Exception as e:
        print("\n✗ Error running agent:")
        print(str(e))

if __name__ == "__main__":
    main()
