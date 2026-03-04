"""Farewell Tool - generates personalized farewells."""

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class FarewellInput(BaseModel):
    """Input schema for farewell tool."""

    name: str = Field(..., description="Name of the person to say goodbye to")
    style: str = Field(
        default="casual",
        description="Farewell style: 'formal', 'casual', or 'enthusiastic'",
    )


class FarewellTool(BaseTool):
    """Generate a personalized farewell."""

    name: str = "farewell"
    description: str = "Generate a personalized farewell for someone"
    args_schema: type[BaseModel] = FarewellInput

    def _run(self, name: str, style: str = "casual") -> str:
        """Generate farewell based on style."""
        farewells = {
            "formal": f"Farewell, {name}. It was a pleasure speaking with you.",
            "casual": f"See ya later, {name}! Take care!",
            "enthusiastic": f"BYE {name}! You're AMAZING! Come back soon! 👋",
        }
        return farewells.get(style, farewells["casual"])
