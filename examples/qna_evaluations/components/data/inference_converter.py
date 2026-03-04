"""Converter for building result rows directly from inference data.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import json
from typing import Any

from rich.console import Console

from .csv_writer import format_tool_execution, format_context_items

console = Console()


def build_result_row_from_inference(
    idx: int,
    data_item: dict[str, Any],
    enriched_data: dict[str, Any],
    manual_review_auto_eval: bool = False,
    max_tools: int = 1,
) -> dict[str, Any]:
    """Build result row directly from inference data without evaluation.
    
    Args:
        idx: Row index (0-based)
        data_item: Original data item with query, expected_answer, etc.
        enriched_data: Enriched data from inference_fn with answer, sources, etc.
        manual_review_auto_eval: Whether to include manual review columns
        max_tools: Maximum number of tool columns to generate
        
    Returns:
        Dictionary with result row data
    """
    # Extract metadata (create_inference_fn stores most data in _metadata)
    metadata = enriched_data.get("_metadata", {})
    
    # Build base result row
    result_row = {
        "Index": idx + 1,
        "Question": data_item.get("query", ""),
        "Expected Answer": data_item.get("expected_answer", data_item.get("expected_response", "")),
        "Requires Visualization": data_item.get("requires_visualization", False),
        "Answer": enriched_data.get("generated_response", ""),
        "Response_Time": metadata.get("execution_time", 0),
    }
    
    # Add manual review columns if needed (before tool columns)
    if manual_review_auto_eval:
        result_row.update({
            "manual_rr": "",
            "issue_category": "",
            "additional_notes": "",
        })
    
    # Generate per-tool columns (source_tool_1, source_tool_2, etc.)
    step_timings = metadata.get("step_timings", [])
    retrieved_context = metadata.get("retrieved_context", [])
    
    # Filter to only finished tool executions (not delegation_start)
    finished_tools = [t for t in step_timings if t.get("status") in ("finished", "delegation_complete")]
    
    # Create per-tool columns
    for tool_idx in range(max_tools):
        tool_col_num = tool_idx + 1
        
        if tool_idx < len(finished_tools):
            tool = finished_tools[tool_idx]
            
            # Format source_tool_N column with full tool details
            formatted_tool = format_tool_execution(tool, tool_idx)
            result_row[f"source_tool_{tool_col_num}"] = formatted_tool
            
            # Format retrieved_context_or_queried_data_N column
            # Find matching context items for this tool
            tool_name = tool.get("tool_name", "")
            tool_context_items = [
                ctx for ctx in retrieved_context
                if isinstance(ctx, dict) and ctx.get("tool_name") == tool_name
            ]
            
            if tool_context_items:
                formatted_context = format_context_items(tool_context_items)
                result_row[f"retrieved_context_or_queried_data_{tool_col_num}"] = formatted_context
            else:
                result_row[f"retrieved_context_or_queried_data_{tool_col_num}"] = ""
        else:
            # Empty columns for consistency across rows
            result_row[f"source_tool_{tool_col_num}"] = ""
            result_row[f"retrieved_context_or_queried_data_{tool_col_num}"] = ""
    
    # Add artifacts column
    result_row["artifacts"] = json.dumps(enriched_data.get("artifacts", []))
    
    # Add error columns at the end
    result_row["evaluation_error"] = ""
    result_row["agent_error"] = metadata.get("error", "")
    
    return result_row
