"""Hello World - Single Agent Example."""
    
from glaip_sdk import Agent
from tools import GreetingTool, time_tool

hello_agent = Agent(
    name="hello_agent",
    instruction="""You are a friendly greeting assistant with knowledge capabilities.""",
    description="A friendly agent that greets users and can explore GitHub repos",
    tools=[GreetingTool, time_tool],
)
hello_agent.deploy()
hello_agent.run("Hello, who are you?")
