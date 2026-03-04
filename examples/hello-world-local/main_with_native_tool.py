"""Hello World - Single Agent Example with Native Tools."""

from glaip_sdk.agents import Agent

tools_list = []
try:
    from aip_agents.tools.web_search import GoogleSerperTool
    tools_list.append(GoogleSerperTool)
except ImportError:
    pass

hello_agent = Agent(
    name="hello_local_agent_with_native_tools",
    instruction="You are a helpful assistant with access to native tools.",
    tools=tools_list,
)

hello_agent.run("Search for the latest news about Barcelona football club.")
