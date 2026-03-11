"""Load visible case notes and store hidden verification data in metadata."""

from __future__ import annotations

from typing import Any

from langchain_core.tools import BaseTool
from langgraph.types import Command
from pydantic import BaseModel, Field

CASE_FILES = {
    "checkout_delay": {
        "public_notes": [
            "Customers are clicking Pay Now more than once because the spinner looks frozen.",
            "Several users think the order failed because the success state appears too late.",
            "Support tickets mention confusion about whether the purchase actually completed.",
        ],
        "hidden_verification_code": "ALPHA-42",
    },
    "onboarding_dropoff": {
        "public_notes": [
            "New users are unsure which task to do first after signup.",
            "The tutorial feels too long, so many users skip it immediately.",
            "Several users want a shorter first-login checklist.",
        ],
        "hidden_verification_code": "BETA-17",
    },
}


class CaseFileInput(BaseModel):
    """Input for loading a case file."""

    case_name: str = Field(default="checkout_delay", description="Case file to load")


class LoadCaseFileTool(BaseTool):
    """Return public notes to the model and store hidden data in metadata."""

    name: str = "load_case_file"
    description: str = (
        "Load a case file. Return public notes in the tool output so the model can read them, "
        "and store the same visible notes plus a hidden verification code in metadata."
    )
    args_schema: type[BaseModel] = CaseFileInput

    def _run(self, case_name: str = "checkout_delay", **kwargs: Any) -> Command:
        del kwargs
        case_file = CASE_FILES.get(case_name, CASE_FILES["checkout_delay"])
        public_notes = case_file["public_notes"]
        public_block = "\n".join(f"- {item}" for item in public_notes)

        return Command(
            update={
                "result": (
                    f"Loaded case file '{case_name}'.\n"
                    "Read the public notes, decide one short summary, then call "
                    "`reveal_verification_code` with only that summary.\n\n"
                    f"Public notes:\n{public_block}"
                ),
                "metadata": {
                    "handoff_state": {
                        "case_name": case_name,
                        "public_notes": public_notes,
                        "hidden_verification_code": case_file[
                            "hidden_verification_code"
                        ],
                    }
                },
            }
        )
