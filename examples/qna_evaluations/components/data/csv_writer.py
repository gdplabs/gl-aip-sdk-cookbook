"""CSV writing and result formatting functionality.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import json
import re
from typing import Any

import pandas as pd
from rich.console import Console

from ..utils import reorder_columns_with_parts, truncate_if_needed

console = Console()


def format_tool_execution(tool: dict[str, Any], tool_idx: int) -> str:
    """Format a tool execution into human-readable string.
    
    Args:
        tool: Tool execution data with tool_name, arguments, output, status, duration_ms
        tool_idx: Tool index for display
        
    Returns:
        Formatted string with tool execution details
    """
    tool_name = tool.get("tool_name", "")
    tool_args = tool.get("arguments", {})
    tool_output = tool.get("output", "")
    tool_status = tool.get("status", "")
    tool_duration = tool.get("duration_ms", "")
    agent_name = tool.get("agent_name", "")
    step_id = tool.get("step_id", "")
    previous_step_ids = tool.get("previous_step_ids", [])
    
    # Determine tool type
    if tool_status == "delegation_start":
        tool_type = "DELEGATION START"
    elif tool_status == "delegation_complete":
        tool_type = "DELEGATION COMPLETE"
    elif "_" in agent_name and not agent_name.count("-") > 3:
        tool_type = "SUB-AGENT TOOL"
    else:
        tool_type = "TOOL"
    
    processed_output = process_tool_output(tool_name, tool_output)
    
    tool_combined = f"[Type: {tool_type}]\n"
    tool_combined += f"[Tool: {tool_name}]\n"
    if agent_name:
        agent_short = agent_name[:50] + "..." if len(agent_name) > 50 else agent_name
        tool_combined += f"[Agent: {agent_short}]\n"
    if step_id:
        tool_combined += f"[Step: {step_id}]\n"
    if previous_step_ids:
        parent_step = previous_step_ids[0] if previous_step_ids else ""
        if parent_step:
            tool_combined += f"[Parent Step: {parent_step}]\n"
    tool_combined += "\n"
    tool_combined += f"**Args:**\n{json.dumps(tool_args, default=str, ensure_ascii=False, indent=2)}\n\n"
    
    if tool_output or tool_status == "finished" or tool_status == "delegation_complete":
        tool_combined += f"**Output:**\n{processed_output}\n\n"
    else:
        tool_combined += "**Output:** (Delegation in progress...)\n\n"
    
    tool_combined += f"**Status:** {tool_status}\n"
    tool_combined += f"**Duration:** {tool_duration}ms"
    
    return truncate_if_needed(tool_combined, max_length=40000, tool_name=tool_name)


def process_tool_output(tool_name: str, tool_output: Any) -> str:
    """Process tool output to extract only relevant content.

    Args:
        tool_name: Name of the tool
        tool_output: Raw tool output

    Returns:
        Processed output string
    """
    processed_output = str(tool_output)

    if "retrieval" in tool_name.lower() and tool_output:
        try:
            if isinstance(tool_output, dict):
                output_data = tool_output
            elif isinstance(tool_output, str):
                try:
                    output_data = json.loads(tool_output)
                except json.JSONDecodeError:
                    json_match = re.search(r"\{.*\}", tool_output, re.DOTALL)
                    if json_match:
                        output_data = json.loads(json_match.group())
                    else:
                        output_data = None
            else:
                output_data = tool_output

            if isinstance(output_data, dict) and "chunks" in output_data:
                chunks = output_data.get("chunks", [])
                if chunks:
                    chunk_contents = []
                    for i, chunk in enumerate(chunks, 1):
                        if isinstance(chunk, dict) and "content" in chunk:
                            chunk_contents.append(f"--- Chunk {i} ---\n{chunk['content']}")

                    if chunk_contents:
                        processed_output = "\n\n".join(chunk_contents)
                        console.print(f"✅ Extracted {len(chunks)} chunks from {tool_name}")
                    else:
                        processed_output = str(tool_output)
                else:
                    processed_output = str(tool_output)
        except Exception as e:
            console.print(f"⚠️  Could not extract chunks from {tool_name}: {e}")
            processed_output = str(tool_output)

    return processed_output


def format_context_items(context_items: list[dict[str, Any]]) -> str:
    """Format retrieved context items into human-readable format.
    
    Args:
        context_items: List of context items from retrieved context.
        
    Returns:
        Formatted string with chunks and query results.
    """
    if not context_items:
        return ""
    
    formatted_parts = []
    chunk_counter = 0
    
    for ctx in context_items:
        ctx_type = ctx.get("type", "")
        
        if ctx_type == "vector_chunk":
            # Vector retrieval chunk
            chunk_counter += 1
            chunk_id = ctx.get("chunk_id", "N/A")
            content = ctx.get("content", "")
            
            truncated_content = truncate_if_needed(content, tool_name=f"vector_chunk_{chunk_counter}")
            
            chunk_part = f"## Chunk {chunk_counter}\n\n"
            chunk_part += f"**Chunk ID:** `{chunk_id}`\n\n"
            chunk_part += f"**Content:**\n```\n{truncated_content}\n```"
            formatted_parts.append(chunk_part)
        
        elif ctx_type == "tool_output_sql_result":
            # SQL query result
            query = ctx.get("query", "")
            results = ctx.get("results", [])
            original_rows = ctx.get("original_rows", len(results) if isinstance(results, list) else 0)
            original_cols = ctx.get("original_cols", 0)
            
            sql_part = ""
            
            if query:
                sql_part += f"**Query:**\n```sql\n{query}\n```\n\n"
            
            if results:
                if isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict):
                    try:
                        df = pd.DataFrame(results)
                        
                        truncated_df = df.iloc[:100, :15]
                        truncated_rows = len(truncated_df)
                        truncated_cols = len(truncated_df.columns)
                        
                        sql_part += "**Results:**\n" + truncated_df.to_markdown(index=False)
                        
                        if original_rows > truncated_rows or original_cols > truncated_cols:
                            sql_part += f"\n\n*(Showing {truncated_rows} of {original_rows} rows, {truncated_cols} of {original_cols} columns)*"
                    except Exception:
                        sql_part += f"**Results:**\n```json\n{json.dumps(results, default=str, ensure_ascii=False, indent=2)}\n```"
                else:
                    sql_part += f"**Results:**\n```json\n{json.dumps(results, default=str, ensure_ascii=False, indent=2)}\n```"
            else:
                sql_part += "**Results:** (empty)"
            
            formatted_parts.append(sql_part)
        
        elif ctx_type == "tool_output_generic":
            content = ctx.get("content", "")
            if content:
                formatted_parts.append(f"**Output:**\n```\n{content}\n```")
    
    return "\n\n".join(formatted_parts) if formatted_parts else ""


def save_results(results: list[dict[str, Any]], output_file: str):
    """Save benchmark results to CSV file.

    Args:
        results: List of result dictionaries
        output_file: Path to output CSV file
    """
    if not results:
        console.print("⚠️  No results to save")
        return

    results_df = pd.DataFrame(results)

    ordered_columns = reorder_columns_with_parts(results_df.columns.tolist())
    results_df = results_df[ordered_columns]

    results_df.to_csv(output_file, index=False)
    console.print(f"\n✅ Results saved to {output_file}")
    console.print(f"   Total rows: {len(results_df)}")
    console.print(f"   Total columns: {len(results_df.columns)}")
