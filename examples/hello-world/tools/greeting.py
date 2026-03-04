"""Greeting Tool - generates personalized greetings."""

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class GreetingInput(BaseModel):
    """Input schema for greeting tool."""

    name: str = Field(..., description="Name of the person to greet")
    style: str = Field(
        default="casual",
        description="Greeting style: 'formal', 'casual', or 'enthusiastic'",
    )


class GreetingTool(BaseTool):
    """Generate a personalized greeting."""

    name: str = "greeting"
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
