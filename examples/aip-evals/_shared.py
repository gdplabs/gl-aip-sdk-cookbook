"""Shared utilities for AIP evals examples."""

import json
from typing import Any


def print_json(data: Any) -> None:
    """Print data in JSON format."""
    print(json.dumps(data, indent=2, default=str))


def warn(message: str) -> None:
    """Print a warning message."""
    print(f"  Warning: {message}")
