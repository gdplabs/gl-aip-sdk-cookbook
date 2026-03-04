"""Hierarchical Pattern (Multi-level Agent Delegation)

This example demonstrates a hierarchical workflow with feedback looping using sub-agents:
Coordinator Agent → Research Agent → Compiler Agent
The coordinator can make decisions based on sub-agent responses.

Usage (from this directory):
    uv run main.py

Note:
    Requires SERPER_API_KEY environment variable for web search functionality.

Authors:
    Putu Ravindra Wiguna (putu.r.wiguna@gdplabs.id)
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from dotenv import load_dotenv
from glaip_sdk import Agent
from glaip_sdk.tools import Tool

load_dotenv(override=True)


# Native tool - will be resolved locally from aip_agents.tools
web_search_tool = Tool.from_native("google_serper")

# Create Research Agent with web search tool
research_agent = Agent(
    name="research_agent",
    instruction="""You are a Research Agent specialized in web searches.
Perform web searches on given topics and provide comprehensive, factual information.
Always use the google_serper tool to gather current information. Return detailed findings with sources.
Only Perform 1 web search maximum per task.
""",
    description="Performs web searches to gather information",
    tools=[web_search_tool],
    model="openai/gpt-5.2",
)

# Create Information Compiler Agent
compiler_agent = Agent(
    name="compiler_agent",
    instruction="""You are an Information Compiler.
Transform raw research data into well-structured, easy-to-read summaries.
Organize information logically, highlight key points, and present in clean markdown format with URLs.""",
    description="Formats and synthesizes research results",
    model="openai/gpt-5.2",
)

# Create Coordinator Agent that manages sub-agents
coordinator_agent = Agent(
    name="coordinator_agent",
    instruction="""You are a Coordinator Agent managing research and compilation tasks.
You have two sub-agents:
1. 'research_agent' - performs web searches and gathers information
2. 'compiler_agent' - compiles and formats research data into summaries

Workflow:
1. Delegate the research topic to 'research_agent' to gather information,
for demo purposes, ask 1 popular topic that will guarantee of output
2. Review the research results
3. Delegate the research data given from 'research_agent' to 'compiler_agent' to create a well-formatted summary
do not ask compiler agent to do web search. Pass on the research result to compiler agent.
4. Return the final compiled summary

Always coordinate both agents in sequence and ensure the final output is comprehensive.""",
    description="Coordinates research and compilation workflow",
    agents=[research_agent, compiler_agent],
    model="openai/gpt-5.2",
)


def main() -> None:
    """Run the hierarchical pattern demo."""
    print("=" * 60)
    print("Hierarchical Pattern Demo (Sub-Agents)")
    print("=" * 60)
    print()
    print("Agent Hierarchy:")
    print("  🎯 Coordinator Agent")
    print("     ├── 🔍 Research Agent (has google_serper tool)")
    print("     └── 📝 Compiler Agent")
    print()
    print("The coordinator delegates to research, then to compiler based on results.")
    print()

    # Example research topic
    research_topic = "Latest developments in artificial intelligence for healthcare in last 6 months"

    print(f"Research Topic: {research_topic}")
    print()
    print("-" * 60)

    # Run the coordinator
    result = coordinator_agent.run(
        f"Research this topic and provide a compiled summary: {research_topic}",
        verbose=False,
    )

    print(result)
    print("\nDemo completed")


if __name__ == "__main__":
    main()
