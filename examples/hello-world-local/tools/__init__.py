"""Tools for local execution demos.

This module contains LangChain BaseTools that can be used in local mode.
This is a LangChain BaseTool that can be used in local mode without @tool_plugin.
The @tool_plugin decorator is optional and only adds metadata for platform deployment.

Authors:
    Christian Trisno Sen Long Chen (christian.t.s.l.chen@gdplabs.id)
"""

from pathlib import Path

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

# =============================================================================
# SimpleGreetingTool
# =============================================================================


class GreetingInput(BaseModel):
    """Input schema for the greeting tool."""

    name: str = Field(description="Name of the person to greet")
    style: str = Field(
        default="casual",
        description="Greeting style: 'formal', 'casual', or 'enthusiastic'",
    )


class SimpleGreetingTool(BaseTool):
    """Generate a personalized greeting.

    This tool works in both local mode and deployed mode.
    No @tool_plugin decorator needed for local execution.
    """

    name: str = "simple_greeting"
    description: str = "Generate a personalized greeting for someone"
    args_schema: type[BaseModel] = GreetingInput

    def _run(self, name: str, style: str = "casual") -> str:
        """Generate greeting based on style."""
        greetings = {
            "formal": f"Good day, {name}. It is a pleasure to meet you.",
            "casual": f"Hey {name}! How's it going?",
            "enthusiastic": f"WOW! {name}! SO GREAT to meet you! 🎉",
        }
        return greetings.get(style, greetings["casual"])


# =============================================================================
# ResearchFormatterTool (with tool_config_schema)
# =============================================================================


class FormatterConfig(BaseModel):
    """Tool configuration for research formatting."""

    style: str = Field(default="brief", description="Output style: brief, detailed, or academic")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum results to format")
    include_links: bool = Field(default=True, description="Include paper links")


class FormatterInput(BaseModel):
    """Input schema for research formatter."""

    query: str = Field(..., description="Research topic or query")


class ResearchFormatterTool(BaseTool):
    """Format research results with configurable style.

    This tool demonstrates tool_config_schema for runtime configuration.
    The config can be set via:
    - Agent(tool_configs={ResearchFormatterTool: {...}})
    - runtime_config={"tool_configs": {ResearchFormatterTool: {...}}}
    """

    name: str = "research_formatter"
    description: str = "Format research papers with configurable output style"
    args_schema: type[BaseModel] = FormatterInput
    tool_config_schema: type[BaseModel] = FormatterConfig

    def _run(self, query: str, config: RunnableConfig | None = None) -> str:
        """Format research results based on configuration."""
        tool_config = self.get_tool_config(config)
        return f"[ResearchFormatter] Query: '{query}' | Config: {tool_config}"


# =============================================================================
# LocalTextFileTool
# =============================================================================


class LocalTextFileInput(BaseModel):
    """Input schema for reading a local text file."""

    file_path: str = Field(description="Path to a local text file")


class LocalTextFileTool(BaseTool):
    """Read a local text file from disk."""

    name: str = "read_local_text_file"
    description: str = "Read a local text file and return its contents"
    args_schema: type[BaseModel] = LocalTextFileInput

    def _run(self, file_path: str) -> str:
        """Return the contents of a local text file."""
        try:
            return Path(file_path).read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ValueError(f"File not found: {file_path}") from exc
        except UnicodeDecodeError as exc:
            raise ValueError(
                f"Could not decode file as UTF-8: {file_path}. Please provide a UTF-8 encoded text file."
            ) from exc
        except OSError as exc:
            raise ValueError(f"Unable to read file: {file_path}. {exc}") from exc


# =============================================================================
# CustomerInfoTool
# =============================================================================


class CustomerInfoInput(BaseModel):
    """Input schema for the customer info tool."""

    customer_id: str = Field(description="Customer ID to look up (e.g., C001, C002, C003)")


class CustomerInfoTool(BaseTool):
    """Retrieve customer information including PII data.

    This tool returns customer data containing:
    - Name
    - Email (PII)
    - Phone (PII)
    - Address (PII)

    When enable_pii=True is set in agent_config at agent construction time,
    these values will be automatically anonymized (e.g., john@example.com -> <EMAIL_1>).
    """

    name: str = "get_customer_info"
    description: str = "Get customer information by customer ID. Returns name, email, phone, and address."
    args_schema: type[BaseModel] = CustomerInfoInput

    CUSTOMER_DATA: dict[str, dict[str, str]] = {
        "C001": {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "phone": "+1-555-0101",
            "address": "123 Main St, New York, NY 10001",
        },
        "C002": {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "phone": "+1-555-0102",
            "address": "456 Oak Ave, Los Angeles, CA 90001",
        },
        "C003": {
            "name": "Bob Williams",
            "email": "bob.williams@example.com",
            "phone": "+1-555-0103",
            "address": "789 Pine Rd, Chicago, IL 60601",
        },
    }

    def _run(self, customer_id: str) -> str:
        """Retrieve customer information."""
        customer = self.CUSTOMER_DATA.get(customer_id.upper())

        if customer:
            return (
                f"Customer {customer_id}:\n"
                f"  Name: {customer['name']}\n"
                f"  Email: {customer['email']}\n"
                f"  Phone: {customer['phone']}\n"
                f"  Address: {customer['address']}"
            )
        return f"Customer {customer_id} not found. Valid IDs: C001, C002, C003"


# =============================================================================
# Tool Output Sharing Tools
# =============================================================================


class GreetingGeneratorInput(BaseModel):
    """Input schema for the greeting generator tool."""

    name: str = Field(description="Name of the person to greet")


class GreetingGeneratorTool(BaseTool):
    """Generate a personalized greeting for tool output sharing demos."""

    name: str = "greeting_generator"
    description: str = "Generate a personalized greeting message"
    args_schema: type[BaseModel] = GreetingGeneratorInput
    store_final_output: bool = True  # Enable automatic storage

    def _run(self, name: str) -> str:
        """Generate a greeting message."""
        return f"Hello, {name}! Welcome to our platform."


class GreetingFormatterInput(BaseModel):
    """Input schema for the greeting formatter tool."""

    message: str = Field(description="Greeting message to format")


class GreetingFormatterTool(BaseTool):
    """Format a greeting message with styling."""

    name: str = "greeting_formatter"
    description: str = "Format a greeting message with styling"
    args_schema: type[BaseModel] = GreetingFormatterInput
    store_final_output: bool = False

    def _run(self, message: str) -> str:
        """Format the greeting message with styling."""
        return f"✨ {message.upper()} ✨"


__all__ = [
    "SimpleGreetingTool",
    "GreetingInput",
    "ResearchFormatterTool",
    "FormatterConfig",
    "FormatterInput",
    "LocalTextFileTool",
    "LocalTextFileInput",
    "CustomerInfoTool",
    "CustomerInfoInput",
    "GreetingGeneratorTool",
    "GreetingGeneratorInput",
    "GreetingFormatterTool",
    "GreetingFormatterInput",
]
