"""Custom metric for artifact and visualization validation.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

from typing import Any

from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import MetricInput, MetricOutput


class ArtifactValidationMetric(BaseMetric):
    """Validate that artifacts are generated when required."""

    name = "artifact_validation"
    required_fields = {"artifacts", "requires_visualization"}
    description = "Validates that visualization artifacts are generated when required"
    good_score = True
    bad_score = False

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        """Evaluate if artifacts were generated when required.

        Args:
            data (MetricInput): The data to evaluate containing artifacts and requires_visualization.

        Returns:
            MetricOutput: Dictionary containing validation results.
        """
        artifacts = data.get("artifacts", [])
        requires_visualization = data.get("requires_visualization", False)
        
        has_artifacts = bool(artifacts and len(artifacts) > 0)
        
        if requires_visualization:
            if has_artifacts:
                return {
                    "score": True,
                    "reason": f"Visualization required and {len(artifacts)} artifact(s) generated",
                    "artifact_count": len(artifacts),
                }
            else:
                return {
                    "score": False,
                    "reason": "Visualization required but no artifacts generated",
                    "artifact_count": 0,
                    "possible_issues": ["Visualization required but no artifacts generated"],
                }
        
        return {
            "score": True,
            "reason": "No visualization required" if not has_artifacts else f"No visualization required, but {len(artifacts)} artifact(s) generated",
            "artifact_count": len(artifacts),
        }
