"""Consume a model summary and reveal hidden metadata from a prior tool."""

from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langgraph.types import Command
from pydantic import BaseModel, Field


class VerificationRevealInput(BaseModel):
    """Input for revealing the hidden verification code."""

    summary: str = Field(description="Short summary produced by the model")


class RevealVerificationCodeTool(BaseTool):
    """Combine a model summary with hidden metadata stored by a prior tool."""

    name: str = "reveal_verification_code"
    description: str = (
        "Take the model summary, then read the stored case data from metadata and reveal "
        "the hidden verification code."
    )
    args_schema: type[BaseModel] = VerificationRevealInput

    def _run(self, summary: str, config: RunnableConfig, **kwargs: object) -> Command:
        del kwargs
        metadata = _read_metadata(config)
        handoff_state = metadata.get("handoff_state", {})
        public_notes = handoff_state.get("public_notes", [])
        case_name = handoff_state.get("case_name", "unknown")
        verification_code = handoff_state.get(
            "hidden_verification_code", "MISSING-CODE"
        )

        public_notes_block = "\n".join(f"- {item}" for item in public_notes) or "- none"

        result = (
            f"Case: {case_name}\n"
            f"Model summary: {summary}\n"
            "Public notes reused from metadata:\n"
            f"{public_notes_block}\n"
            f"Hidden verification code from metadata: {verification_code}"
        )

        scrubbed_metadata = dict(metadata)
        scrubbed_metadata["handoff_state"] = {
            "case_name": case_name,
            "public_notes": public_notes,
            "consumed": True,
        }

        return Command(update={"result": result, "metadata": scrubbed_metadata})


def _read_metadata(config: RunnableConfig) -> dict[str, Any]:
    metadata = config.get("metadata")
    if isinstance(metadata, dict):
        return metadata

    return {}
