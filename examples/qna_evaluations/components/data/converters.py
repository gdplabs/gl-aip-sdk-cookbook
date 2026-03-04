"""Converters for transforming experiment tracker results to benchmark format.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import json
from typing import Any

import pandas as pd
from rich.console import Console

from .csv_writer import format_tool_execution, format_context_items

console = Console()


def calculate_max_tools(df_results: pd.DataFrame) -> int:
    """Calculate maximum number of tools across all rows.
    
    Args:
        df_results: DataFrame from experiment tracker CSV
        
    Returns:
        Maximum number of tools found
    """
    max_tools = 0
    for _, row in df_results.iterrows():
        try:
            data_str = row.get("data", "{}")
            data_json = json.loads(data_str) if isinstance(data_str, str) else data_str
            metadata = data_json.get("_metadata", {})
            step_timings = metadata.get("step_timings", [])
            max_tools = max(max_tools, len(step_timings))
        except Exception:
            pass
    return max_tools


def extract_geval_data(geval_scores: list, result_idx: int, row: Any) -> dict[str, Any]:
    """Extract GEval evaluation data from scores list.
    
    Args:
        geval_scores: List of GEval score dictionaries
        result_idx: Current result index (1-based)
        row: DataFrame row with additional evaluation data
        
    Returns:
        Dictionary with evaluation metrics
    """
    eval_data = {}
    geval_data = geval_scores[result_idx - 1] if result_idx - 1 < len(geval_scores) else None
    
    if geval_data and isinstance(geval_data, dict):
        # Extract completeness
        completeness = geval_data.get("completeness", {})
        eval_data["geval_completeness"] = completeness.get("score") if isinstance(completeness, dict) else None
        eval_data["geval_completeness_explanation"] = completeness.get("explanation", "") if isinstance(completeness, dict) else ""
        
        # Extract groundedness
        groundedness = geval_data.get("groundedness", {})
        eval_data["geval_groundedness"] = groundedness.get("score") if isinstance(groundedness, dict) else None
        eval_data["geval_groundedness_explanation"] = groundedness.get("explanation", "") if isinstance(groundedness, dict) else ""
        
        # Extract redundancy
        redundancy = geval_data.get("redundancy", {})
        eval_data["geval_redundancy"] = redundancy.get("score") if isinstance(redundancy, dict) else None
        eval_data["geval_redundancy_explanation"] = redundancy.get("explanation", "") if isinstance(redundancy, dict) else ""
        
        # Extract language_consistency
        language_consistency = geval_data.get("language_consistency", {})
        eval_data["geval_language_consistency"] = language_consistency.get("score") if isinstance(language_consistency, dict) else None
        eval_data["geval_language_consistency_explanation"] = language_consistency.get("explanation", "") if isinstance(language_consistency, dict) else ""
        
        # Extract refusal_alignment
        refusal_alignment = geval_data.get("refusal_alignment", {})
        eval_data["geval_refusal_alignment"] = refusal_alignment.get("score") if isinstance(refusal_alignment, dict) else None
        eval_data["geval_refusal_alignment_explanation"] = refusal_alignment.get("explanation", "") if isinstance(refusal_alignment, dict) else ""
        
        # Extract auto_rr and possible_issues
        eval_data["auto_rr"] = geval_data.get("relevancy_rating")
        geval_issues = geval_data.get("possible_issues", [])
        
        # Check artifact validation from evaluation results
        artifact_issues = []
        if row.get("artifact_validation.score") == False or row.get("artifact_validation.score") == "False":
            artifact_issues.append("Visualization required but no artifacts generated")
        
        # Merge all possible issues
        all_issues = list(geval_issues) + artifact_issues
        eval_data["possible_issues"] = ", ".join(all_issues) if all_issues else ""
    else:
        # No GEval data available
        eval_data["geval_completeness"] = None
        eval_data["geval_completeness_explanation"] = ""
        eval_data["geval_groundedness"] = None
        eval_data["geval_groundedness_explanation"] = ""
        eval_data["geval_redundancy"] = None
        eval_data["geval_redundancy_explanation"] = ""
        eval_data["geval_language_consistency"] = None
        eval_data["geval_language_consistency_explanation"] = ""
        eval_data["geval_refusal_alignment"] = None
        eval_data["geval_refusal_alignment_explanation"] = ""
        eval_data["auto_rr"] = None
        eval_data["possible_issues"] = ""
    
    return eval_data


def process_experiment_row(
    row: Any,
    result_idx: int,
    max_tools: int,
    manual_review_auto_eval: bool,
    geval_scores: list,
) -> dict[str, Any]:
    """Process a single experiment tracker row into result format.
    
    Args:
        row: DataFrame row from experiment tracker
        result_idx: Result index (1-based)
        max_tools: Maximum number of tools to pre-allocate columns
        manual_review_auto_eval: Whether to use detailed manual review columns
        geval_scores: List of GEval score dictionaries
        
    Returns:
        Dictionary with result row data
    """
    # Parse JSON from 'data' column
    data_json = {}
    try:
        data_str = row.get("data", "{}")
        if isinstance(data_str, str):
            data_json = json.loads(data_str)
        elif isinstance(data_str, dict):
            data_json = data_str
    except Exception as e:
        console.print(f"[yellow]Warning: Could not parse data JSON: {e}[/yellow]")
    
    # Extract metadata
    metadata = data_json.get("_metadata", {})
    
    # Build base result row
    result_row = {
        "Index": result_idx,
        "Question": data_json.get("query", ""),
        "Expected Answer": data_json.get("expected_response", ""),
        "Requires Visualization": data_json.get("requires_visualization", False),
        "Answer": data_json.get("generated_response", ""),
        "Response_Time": metadata.get("execution_time", 0) if isinstance(metadata, dict) else 0,
    }
    
    # Add manual review columns if needed (before tool columns)
    if manual_review_auto_eval:
        result_row.update({
            "manual_rr": "",
            "issue_category": "",
            "additional_notes": "",
        })
    
    # Generate per-tool columns (source_tool_1, source_tool_2, etc.)
    step_timings = metadata.get("step_timings", []) if isinstance(metadata, dict) else []
    retrieved_context = metadata.get("retrieved_context", []) if isinstance(metadata, dict) else []
    
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
    result_row["artifacts"] = json.dumps(data_json.get("artifacts", []))
    
    # Add evaluation metrics
    eval_data = extract_geval_data(geval_scores, result_idx, row)
    result_row.update(eval_data)
    
    # Add error columns at the end
    result_row["evaluation_error"] = ""
    result_row["agent_error"] = metadata.get("error", "") if isinstance(metadata, dict) else ""
    
    return result_row


def convert_experiment_tracker_results(
    df_results: pd.DataFrame,
    manual_review_auto_eval: bool = False,
    geval_scores: list[dict[str, Any] | None] = None,
) -> list[dict[str, Any]]:
    """Convert experiment tracker CSV results to benchmark CSV format.
    
    Args:
        df_results: DataFrame from experiment tracker CSV
        manual_review_auto_eval: Whether to use detailed manual review columns
        geval_scores: List of GEval score dictionaries from evaluation_result["results"]
    
    Returns:
        List of result dictionaries for CSV output
    """
    geval_scores = geval_scores or []
    
    # Calculate max tools across all rows
    max_tools = calculate_max_tools(df_results)
    console.print(f"📊 Max tools found across all rows: {max_tools}")
    
    # Process each row
    results = []
    for result_idx, (df_idx, row) in enumerate(df_results.iterrows(), 1):
        result_row = process_experiment_row(
            row=row,
            result_idx=result_idx,
            max_tools=max_tools,
            manual_review_auto_eval=manual_review_auto_eval,
            geval_scores=geval_scores,
        )
        results.append(result_row)
    
    return results
