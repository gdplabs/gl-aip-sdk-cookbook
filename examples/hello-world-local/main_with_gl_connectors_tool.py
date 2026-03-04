"""Hello World - Single Agent Example with GL Connector Tools."""

from aip_agents.tools.gl_connector import GLConnectorTool
from glaip_sdk.agents import Agent

hello_agent = Agent(
    name="hello_local_agent_with_gl_connector_tools",
    instruction="You are a helpful assistant with access to GL Connectors.",
    tools=[GLConnectorTool("github_list_pull_requests_tool")],
)

hello_agent.run("List the most recent pull requests for gdp-admin/gl-connector.")
