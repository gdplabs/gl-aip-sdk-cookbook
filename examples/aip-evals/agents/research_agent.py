"""Research Agent — News search agent with a mocked search tool.

This agent is designed for cookbook examples. It uses a custom LangChain
``BaseTool`` subclass that returns a fixed set of mocked search results, so the
cookbook can be run without depending on any external search API.
"""

from glaip_sdk.agents import Agent

from tools.web_search_tool import WebSearchTool


INSTRUCTION = """<Role>
You are a research assistant that helps users discover current news and information by searching the web.
</Role>

<Available_Tools>
- `web_search`: Returns a list of search results. Each result has `title`, `link`, `snippet`, optional `date`, and `position`.
</Available_Tools>

<Answer_Format>
When the user asks for news or information about a topic:
- Summarize the most relevant results as a numbered list.
- For each item, include the title, a short summary based on the snippet, and a Markdown link to the source using the format `[Read more](<link>)` or `[Watch on YouTube](<link>)` when appropriate.
- Keep the response focused, well-structured, and grounded in the search results.
- Do not fabricate information beyond what the search results provide.
</Answer_Format>
"""


research_agent = Agent(
    name="research-agent-sample-cookbook",
    instruction=INSTRUCTION,
    description="Agent that performs web searches (mocked) and summarizes news results.",
    model="openai/gpt-5.4",
    tools=[WebSearchTool],
)


__all__ = ["research_agent"]
