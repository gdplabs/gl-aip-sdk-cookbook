import os
from datetime import datetime, timezone
from calendar import monthrange
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from glaip_sdk import Agent, MCP
from glaip_sdk.models.filesystem import LocalDiskConfig
from gl_connectors_sdk import GLConnectors
from gl_connectors_sdk.models.file import ConnectorFile

load_dotenv()

# =============================================================================
# API (Surgical) — Upload a local file to Google Drive via GL Connectors SDK
# Hits POST /connectors/google_drive/create_file with a ConnectorFile payload.
# No `parent_folder_id` is sent, so the file lands in the user's My Drive root.
# A direct API call is necessary here: MCP cannot carry binary file uploads.
# =============================================================================
class GoogleDriveUploadInput(BaseModel):
    path: str = Field(..., description="Absolute path of the local file to upload.")
    content_type: str = Field("application/octet-stream", description="MIME type of the file.")


class GoogleDriveUploadTool(BaseTool):
    name: str = "google_drive_upload_file_api"
    description: str = (
        "Upload a local file to the current user's Google Drive (My Drive root). "
        "Returns the created file's metadata (id, name, ...)."
    )
    args_schema: type[BaseModel] = GoogleDriveUploadInput

    def _run(self, path: str, content_type: str = "application/octet-stream") -> dict[str, Any]:
        file_path = Path(path)
        connector_file = ConnectorFile(
            file=file_path.read_bytes(),
            filename=file_path.name,
            content_type=content_type,
        )
        connector = GLConnectors(api_base_url="https://connectors.glair.ai")
        data, _ = connector.execute(
            "google_drive",
            "create_file",
            token=os.getenv("GL_CONNECTORS_USER_TOKEN"),
            input_={"file": connector_file},
        )
        return data


# =============================================================================
# Function Calling — date math + local filesystem helpers the LLM can't do reliably
# =============================================================================
class _EmptyInput(BaseModel):
    pass


class GetMonthDateRangeTool(BaseTool):
    name: str = "get_month_date_range"
    description: str = (
        "Return the current calendar month's start and end dates in UTC, both inclusive, "
        "formatted as YYYY-MM-DD. Use this to scope queries to 'this month'."
    )
    args_schema: type[BaseModel] = _EmptyInput

    def _run(self) -> dict[str, str]:
        now = datetime.now(timezone.utc)
        last_day = monthrange(now.year, now.month)[1]
        return {
            "start": f"{now.year:04d}-{now.month:02d}-01",
            "end": f"{now.year:04d}-{now.month:02d}-{last_day:02d}",
        }


class WriteTempFileInput(BaseModel):
    filename: str = Field(..., description="File name (basename only, no directories).")
    content: str = Field(..., description="Text content to write.")


class WriteTempFileTool(BaseTool):
    name: str = "write_temp_file"
    description: str = "Write text content to /tmp/<filename> and return the absolute path."
    args_schema: type[BaseModel] = WriteTempFileInput

    def _run(self, filename: str, content: str) -> str:
        safe_name = Path(filename).name
        out = Path("/tmp") / safe_name
        out.write_text(content, encoding="utf-8")
        return str(out)


class DeleteFileInput(BaseModel):
    path: str = Field(..., description="Absolute path of the file to delete.")


class DeleteFileTool(BaseTool):
    name: str = "delete_file"
    description: str = "Delete a file at the given absolute path."
    args_schema: type[BaseModel] = DeleteFileInput

    def _run(self, path: str) -> str:
        Path(path).unlink(missing_ok=True)
        return f"deleted {path}"


# =============================================================================
# MCP — GitHub, locked to a single tool: github_list_pull_requests
# =============================================================================
github_mcp = MCP(
    name="github",
    transport="http",
    config={"url": "https://connectors.glair.ai/github/mcp"},
)

# =============================================================================
# Skill — local folder. The SKILL.md drives the orchestration + output format.
# =============================================================================
SKILL_PATH = "https://github.com/gdplabs/gl-aip-sdk-cookbook/tree/main/examples/gl-connectors-examples/example-skill"

# =============================================================================
# Agent — each integration owns one distinct role in the pipeline:
#   API (surgical)   -> upload to Google Drive
#   Function Calling -> date range, temp file write/delete
#   MCP              -> fetch PRs (only)
#   Skill            -> orchestrates the flow and defines the output format
# =============================================================================
agent = Agent(
    name="aip_with_pr_summary_pipeline",
    instruction=(
        "You are a PR reporting assistant. For PR summary requests, follow the "
        "'pr-monthly-summary' skill end to end — it owns the workflow and output format."
    ),
    tools=[
        GoogleDriveUploadTool(),
        GetMonthDateRangeTool(),
        WriteTempFileTool(),
        DeleteFileTool(),
    ],
    mcps=[github_mcp],
    mcp_configs={
        github_mcp: {
            "allowed_tools": ["github_list_pull_requests"],
            "authentication": {
                "type": "bearer-token",
                "token": os.getenv("GL_CONNECTORS_USER_TOKEN"),
            },
        }
    },
    skills=[SKILL_PATH],
    filesystem=LocalDiskConfig(
        base_directory="/tmp/agent_files",
        allow_execute=True,
    ),
)

response = agent.run("Summarize PRs from gdplabs/gl-aip-sdk-cookbook within this month.")
print(response)
