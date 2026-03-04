"""Hello World - Single Agent Example with Document Processing (PDF)."""

from pathlib import Path

from glaip_sdk.agents import Agent

try:
    from aip_agents.tools.document_loader import PDFReaderTool
    tools_list = [PDFReaderTool]
except ImportError:
    tools_list = []

file_agent = Agent(
    name="hello_local_agent_with_pdf",
    instruction="You are a helpful assistant with access to PDF document processing.",
    tools=tools_list,
)

base_dir = Path(__file__).resolve().parent
local_file = base_dir / "files" / "example.pdf"
file_agent.run("Please read the provided local pdf file and summarize it.", files=[str(local_file)])
