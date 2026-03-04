"""Utility functions for the benchmark system.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import json
import threading
from typing import Any

from rich.console import Console

console = Console()
_print_lock = threading.Lock()


def thread_safe_print(*args, **kwargs):
    """Thread-safe print function for parallel execution.

    Args:
        *args: Positional arguments to pass to console.print
        **kwargs: Keyword arguments to pass to console.print
    """
    with _print_lock:
        console.print(*args, **kwargs)


def reorder_columns_with_parts(columns: list[str]) -> list[str]:
    """Reorder columns so that _part_2, _part_3, etc. are adjacent to their base columns,
    and source_tool columns appear after Response_Time (before retrieved_context).

    Args:
        columns: List of column names

    Returns:
        List of reordered column names
    """
    base_cols = []
    part_cols = {}
    source_tool_cols = []

    for col in columns:
        if "_part_" in col:
            base = col.split("_part_")[0]
            if base not in part_cols:
                part_cols[base] = []
            part_cols[base].append(col)
        elif col.startswith("source_tool_"):
            source_tool_cols.append(col)
        else:
            base_cols.append(col)

    source_tool_cols.sort(key=lambda x: int(x.split("_")[-1]) if x.split("_")[-1].isdigit() else 0)

    ordered = []
    source_tools_added = False
    
    for col in base_cols:
        ordered.append(col)

        # Add source_tool columns after Response_Time or manual review columns
        if not source_tools_added and source_tool_cols:
            if col in ("Response_Time", "additional_notes", "manual_groundedness"):
                ordered.extend(source_tool_cols)
                source_tools_added = True

        if col in part_cols:
            sorted_parts = sorted(part_cols[col], key=lambda x: int(x.split("_part_")[1]))
            ordered.extend(sorted_parts)
    
    # If source_tool columns weren't added yet, add them at the end before evaluation columns
    if not source_tools_added and source_tool_cols:
        # Find position before geval columns or at the end
        insert_pos = len(ordered)
        for i, col in enumerate(ordered):
            if col.startswith("geval_") or col.startswith("auto_rr"):
                insert_pos = i
                break
        for j, source_col in enumerate(source_tool_cols):
            ordered.insert(insert_pos + j, source_col)

    return ordered


def truncate_if_needed(data: str, max_length: int = 20000, tool_name: str = "unknown") -> str:
    """Truncate data if it exceeds max_length and print warning.

    Args:
        data: Text data to truncate
        max_length: Maximum allowed length
        tool_name: Name of tool for warning message

    Returns:
        Truncated data
    """
    if len(data) > max_length:
        thread_safe_print(f"⚠️  Truncated {tool_name} output from {len(data):,} to {max_length:,} chars")
        return data[:max_length]
    return data


