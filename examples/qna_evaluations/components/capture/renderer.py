"""Renderers for capturing agent execution data.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import ast
import json
import re
import time
from datetime import datetime
from io import StringIO
from typing import Any

from glaip_sdk.utils.run_renderer import RichStreamRenderer, RunStats
from rich.console import Console

console = Console()


def sanitize_unquoted_tokens(text: str) -> str:
    """Sanitize unquoted angle bracket tokens like <MONEY_*> in JSON/Python literal strings.
    
    This token is produced by PII masking and causing issues with JSON parsing.
    
    Args:
        text: The text to sanitize.
        
    Returns:
        Sanitized text with angle bracket tokens properly quoted.
    """
    token_pattern = r"(?:\d+\.)?<[A-Z_][A-Za-z0-9_]*>(?:\.\d+)?"
    
    def sanitize_outside_strings(segment: str) -> str:
        # Pattern 1: Tokens after colons (dict values): ": <TOKEN>" or ": <TOKEN>,
        segment = re.sub(
            r"(:\s*)(" + token_pattern + r")(\s*[,\}\]])",
            "\\1\"\\2\"\\3",
            segment,
        )
        
        # Pattern 2: Tokens in arrays/lists: "[..., <TOKEN>, ...]" or "[..., <TOKEN>]"
        segment = re.sub(
            r"([\[,]\s*)(" + token_pattern + r")(\s*[,\]])",
            "\\1\"\\2\"\\3",
            segment,
        )
        
        # Pattern 3: Tokens at start of array: "[<TOKEN>"
        segment = re.sub(
            r"(\[\s*)(" + token_pattern + r")",
            "\\1\"\\2\"",
            segment,
        )
        
        return segment
    
    parts = []
    start = 0
    in_string = False
    escape = False
    
    for i, ch in enumerate(text):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == "\"":
            if in_string:
                parts.append((True, text[start:i + 1]))
                start = i + 1
                in_string = False
            else:
                if start < i:
                    parts.append((False, text[start:i]))
                start = i
                in_string = True
    
    if start < len(text):
        parts.append((in_string, text[start:]))
    
    sanitized_parts = []
    for is_string, segment in parts:
        if is_string:
            sanitized_parts.append(segment)
        else:
            sanitized_parts.append(sanitize_outside_strings(segment))
    
    return "".join(sanitized_parts)


class OptimizedCLIAgentRenderer(RichStreamRenderer):
    """Optimized renderer for capturing essential agent execution data."""

    def __init__(self):
        """Initialize the renderer with silent console for data capture."""
        silent_file = StringIO()
        silent_console = Console(file=silent_file, quiet=True, width=120)
        super().__init__(console=silent_console, verbose=True)

        self.captured_trajectory = []
        self.captured_thinking_steps = []
        self.captured_retrieved_context = []
        self.captured_sources = []
        self.captured_tool_executions = []
        self.captured_raw_events = []
        self.captured_artifacts = []
        self.final_response = ""
        self.execution_metadata = {}
        self.start_time = time.time()
        self.error_occurred = False
        self.error_details = {}
        self.tool_start_times = {}

    def on_event(self, ev: dict[str, Any]) -> None:
        """Capture events and extract essential information.

        Args:
            ev: Event dictionary from the SDK
        """
        try:
            super().on_event(ev)

            current_time = time.time()
            relative_time = current_time - self.start_time

            event_copy = {
                "timestamp": current_time,
                "relative_time": relative_time,
                "event_data": json.loads(json.dumps(ev, default=str)),
            }
            self.captured_raw_events.append(event_copy)

            metadata = ev.get("metadata", {})
            kind = metadata.get("kind", "")
            content = ev.get("content", "")

            if kind in ["agent_thinking_step", "final_agent_thinking_step", "thinking", "reasoning"]:
                if content:
                    thinking_data = self._create_thinking_data(
                        content=content,
                        kind=kind,
                        timestamp=datetime.fromtimestamp(current_time).isoformat(),
                        relative_time=relative_time,
                    )
                    self.captured_thinking_steps.append(thinking_data)

            if kind == "agent_thinking_step":
                tool_info = metadata.get("tool_info", {})

                if "tool_calls" in tool_info and isinstance(tool_info.get("tool_calls"), list):
                    for tool_call in tool_info["tool_calls"]:
                        tool_name = tool_call.get("name", "")
                        if "delegate_to_" in tool_name:
                            tool_id = tool_call.get("id", f"tool_{len(self.captured_tool_executions)}")
                            self.tool_start_times[tool_id] = current_time

                            delegation_start = {
                                "tool_name": tool_name,
                                "arguments": tool_call.get("args", {}),
                                "output": "",
                                "status": "delegation_start",
                                "duration_ms": 0,
                                "step_id": metadata.get("step_id", tool_id),
                                "tool_id": tool_id,
                                "agent_name": metadata.get("agent_name", ""),
                                "previous_step_ids": metadata.get("previous_step_ids", []),
                                "timestamp": datetime.fromtimestamp(current_time).isoformat(),
                            }
                            self.captured_tool_executions.append(delegation_start)

                if "name" in tool_info and "output" in tool_info:
                    tool_name = tool_info.get("name", "unknown")
                    tool_id = tool_info.get("id", f"tool_{len(self.captured_tool_executions)}")
                    is_delegation = "delegate_to_" in tool_name

                    execution_time_s = tool_info.get("execution_time", 0)
                    duration_ms = int(execution_time_s * 1000) if execution_time_s else 0

                    tool_completion = {
                        "tool_name": tool_name,
                        "arguments": tool_info.get("args", {}),
                        "output": tool_info.get("output", ""),
                        "status": "delegation_complete" if is_delegation else "finished",
                        "duration_ms": duration_ms,
                        "step_id": metadata.get("step_id", tool_id),
                        "tool_id": tool_id,
                        "agent_name": metadata.get("agent_name", ""),
                        "previous_step_ids": metadata.get("previous_step_ids", []),
                        "timestamp": datetime.fromtimestamp(current_time).isoformat(),
                    }
                    self.captured_tool_executions.append(tool_completion)
                    
                    # Extract retrieved context from tool outputs
                    self._extract_context_from_tool_output(tool_name, tool_info.get("output", ""), metadata)

            if kind == "final_response":
                final_content = ev.get("content", "")
                references = metadata.get("references", [])

                if references:
                    for i, ref in enumerate(references):
                        if ref:
                            essential_ref = {
                                "type": "final_response_reference",
                                "reference_index": i,
                                "id": ref.get("id", ""),
                                "title": ref.get("title", ""),
                                "content": ref.get("content", ""),
                                "source": ref.get("source", ""),
                            }

                            self.captured_retrieved_context.append(essential_ref)

                            if essential_ref["content"]:
                                title = essential_ref["title"]
                                source = essential_ref["source"]
                                header = (
                                    f"[Reference {i + 1}]"
                                    + (f" {title}" if title else "")
                                    + (f" from {source}" if source else "")
                                )
                                formatted_content = f"{header}\n{essential_ref['content']}"
                                if formatted_content not in self.captured_sources:
                                    self.captured_sources.append(formatted_content)

                self.final_response = final_content

            # Capture any other content that might be thinking/reasoning (matching original)
            if content and len(content) > 50 and kind != "final_response":
                if self._is_thinking_content(content):
                    thinking_data = self._create_thinking_data(
                        content=content,
                        kind=f"inferred_thinking_{kind}",
                        timestamp=datetime.fromtimestamp(current_time).isoformat(),
                        relative_time=relative_time,
                    )
                    self.captured_thinking_steps.append(thinking_data)

            artifacts = ev.get("artifacts", [])
            if artifacts:
                for artifact in artifacts:
                    artifact_data = {
                        "artifact_id": artifact.get("artifact_id", ""),
                        "name": artifact.get("name", ""),
                        "file_name": artifact.get("file_name", ""),
                        "content_type": artifact.get("content_type", ""),
                        "mime_type": artifact.get("mime_type", ""),
                        "file_uri": artifact.get("file_uri", ""),
                        "timestamp": datetime.fromtimestamp(current_time).isoformat(),
                    }
                    self.captured_artifacts.append(artifact_data)

        except Exception as e:
            error_event = {
                "timestamp": time.time(),
                "kind": "parsing_error",
                "error": str(e),
                "original_event_kind": ev.get("metadata", {}).get("kind", "unknown"),
            }
            self.captured_raw_events.append(error_event)

    def on_complete(self, stats: RunStats) -> None:
        """Capture completion data.

        Args:
            stats: Run statistics from the SDK
        """
        try:
            final = "".join(self.buffer) if hasattr(self, "buffer") else ""

            if final and not self.final_response:
                self.final_response = final

            self.execution_metadata = {
                "duration_s": stats.duration_s if hasattr(stats, "duration_s") else None,
                "finished_at": time.time(),
                "total_events": len(self.captured_raw_events),
                "thinking_steps_count": len(self.captured_thinking_steps),
                "trajectory_steps_count": len(self.captured_trajectory),
                "tool_executions_count": len(self.captured_tool_executions),
                "retrieved_context_count": len(self.captured_retrieved_context),
            }

            # Extract tool executions from steps (fallback if not captured during events)
            self._extract_tool_executions()
            
            self._extract_retrieved_context_from_tools()

            self._ensure_comprehensive_thinking_data()

            try:
                super().on_complete(stats)
            except Exception as parent_error:
                console.print(f"[yellow]Warning in parent on_complete: {parent_error}[/yellow]")

        except Exception as e:
            console.print(f"[yellow]Warning in on_complete: {e}[/yellow]")

    def _create_thinking_data(self, content: str, kind: str, timestamp=None, relative_time=None) -> dict[str, Any]:
        """Create a standardized thinking data structure.

        Args:
            content: Thinking content text
            kind: Type of thinking step
            timestamp: ISO timestamp
            relative_time: Time relative to start

        Returns:
            Dictionary with thinking step data
        """
        return {
            "timestamp": timestamp or datetime.now().isoformat(),
            "content": content,
            "kind": kind,
            "relative_time": relative_time if relative_time is not None else time.time() - self.start_time,
        }

    def _is_thinking_content(self, content: str) -> bool:
        """Check if content looks like thinking/reasoning.
        
        Args:
            content: Text content to check
            
        Returns:
            True if content appears to be thinking/reasoning
        """
        if not content or len(content) < 20:
            return False
        thinking_keywords = ["let me", "i need to", "i should", "i will", "thinking", 
                           "analyzing", "considering", "based on", "according to"]
        return any(keyword in content.lower() for keyword in thinking_keywords)

    def _ensure_comprehensive_thinking_data(self):
        """Ensure we have comprehensive thinking data even if not explicitly captured."""
        try:
            # If we don't have thinking steps, try to extract from raw events
            if not self.captured_thinking_steps:
                for event in self.captured_raw_events:
                    event_data = event.get("event_data", {})
                    content = event_data.get("content", "")
                    kind = event_data.get("metadata", {}).get("kind", "")
                    
                    if self._is_thinking_content(content):
                        thinking_data = self._create_thinking_data(
                            content=content,
                            kind=f"extracted_thinking_{kind}",
                            timestamp=event.get("timestamp"),
                            relative_time=event.get("relative_time")
                        )
                        self.captured_thinking_steps.append(thinking_data)
            
            # If still no thinking steps, create a summary from trajectory
            if not self.captured_thinking_steps and self.captured_trajectory:
                summary_content = f"Agent executed {len(self.captured_trajectory)} trajectory steps with {len(self.captured_tool_executions)} tool executions"
                summary_thinking = self._create_thinking_data(content=summary_content, kind="execution_summary")
                self.captured_thinking_steps.append(summary_thinking)

        except Exception as e:
            console.print(f"[yellow]Warning ensuring thinking data: {e}[/yellow]")
    
    def _extract_tool_executions(self):
        """Extract tool execution information from steps (fallback if not captured during events).
        
        This method iterates through self.steps.by_id to extract tool executions
        after completion, matching the original benchmark logic.
        """
        try:
            for step_id, step in self.steps.by_id.items():
                if step.kind == "tool":
                    # Check if we already have this tool execution captured
                    existing_tool_names = [t.get("tool_name") for t in self.captured_tool_executions]
                    if step.name in existing_tool_names:
                        continue
                    
                    # Extract tool execution data
                    tool_execution = {
                        "tool_name": step.name,
                        "arguments": step.args,
                        "output": step.output[:1000] + "..." if len(step.output) > 1000 else step.output,
                        "status": step.status,
                        "duration_ms": step.duration_ms,
                        "step_id": step_id,
                        "timestamp": datetime.fromtimestamp(step.started_at).isoformat() if hasattr(step, 'started_at') else datetime.now().isoformat()
                    }
                    self.captured_tool_executions.append(tool_execution)
                    
                    # Add to trajectory for compatibility
                    self.captured_trajectory.append({
                        "step_type": "tool_execution",
                        "tool_name": step.name,
                        "status": step.status,
                        "duration_ms": step.duration_ms,
                        "timestamp": tool_execution["timestamp"]
                    })
                    
                    # Extract context from tool output if it looks like retrieval
                    if step.output and ("retrieval" in step.name.lower() or "search" in step.name.lower() or "hybrid" in step.name.lower()):
                        self._extract_retrieval_data_from_output(step.output, step.name)
                        
        except Exception as e:
            console.print(f"[yellow]Warning extracting tool executions: {e}[/yellow]")
    
    def _extract_context_from_tool_output(self, tool_name: str, tool_output: Any, metadata: dict[str, Any]) -> None:
        """Extract retrieved context from tool outputs (SQL, Vector DB, etc.).
        
        Args:
            tool_name: Name of the tool.
            tool_output: Raw tool output.
            metadata: Event metadata.
        """
        try:
            if not tool_output:
                return
            
            step_id = metadata.get("step_id", "")
            agent_name = metadata.get("agent_name", "")
            
            # Extract context based on tool type
            if "sql" in tool_name.lower() or "query" in tool_name.lower():
                self._extract_sql_context(tool_name, tool_output, step_id, agent_name, metadata)
            elif "vector" in tool_name.lower() or "search" in tool_name.lower() or "retrieval" in tool_name.lower():
                self._extract_vector_context(tool_name, tool_output, step_id, agent_name)
        except Exception as e:
            console.print(f"[yellow]Warning extracting context from {tool_name}: {e}[/yellow]")
    
    def _extract_sql_context(self, tool_name: str, tool_output: Any, step_id: str, agent_name: str, metadata: dict[str, Any]) -> None:
        """Extract SQL query results as retrieved context."""
        try:
            # Extract query from metadata if available (Branch A format)
            query = ""
            tool_info = metadata.get("tool_info", {})
            if tool_info:
                args = tool_info.get("args", {})
                request = args.get("request", {})
                query = request.get("query", "")
            
            # Parse tool output if string
            if isinstance(tool_output, str):
                try:
                    sanitized_output = sanitize_unquoted_tokens(tool_output)
                    tool_output = ast.literal_eval(sanitized_output)
                except (ValueError, SyntaxError):
                    return
            
            # Capture both non-empty AND empty SQL results (important for eval to know query was executed)
            if isinstance(tool_output, list):
                # Calculate original dimensions
                original_rows = len(tool_output)
                original_cols = 0
                if tool_output and len(tool_output) > 0 and isinstance(tool_output[0], dict):
                    original_cols = len(tool_output[0].keys())
                
                context_entry = {
                    "type": "tool_output_sql_result",
                    "tool_name": tool_name,
                    "query": query,  # Include SQL query text even for empty results
                    "results": tool_output,  # Empty list [] for no results
                    "original_rows": original_rows,
                    "original_cols": original_cols,
                    "step_id": step_id,
                    "agent_name": agent_name,
                    "timestamp": datetime.now().isoformat(),
                }
                self.captured_retrieved_context.append(context_entry)
        except Exception as e:
            console.print(f"[yellow]Warning extracting SQL context: {e}[/yellow]")
    
    def _extract_vector_context(self, tool_name: str, tool_output: Any, step_id: str, agent_name: str) -> None:
        """Extract chunks from vector tool outputs."""
        try:
            output_data = None
            
            if isinstance(tool_output, dict):
                output_data = tool_output
            elif isinstance(tool_output, str):
                sanitized_output = sanitize_unquoted_tokens(tool_output)
                try:
                    output_data = ast.literal_eval(sanitized_output)
                except (ValueError, SyntaxError):
                    try:
                        output_data = json.loads(sanitized_output)
                    except json.JSONDecodeError:
                        return
            
            if output_data and isinstance(output_data, dict):
                chunks = output_data.get("chunks", [])
                if chunks:
                    for chunk in chunks:
                        if isinstance(chunk, dict) and chunk.get("content"):
                            context_entry = {
                                "type": "vector_chunk",
                                "tool_name": tool_name,
                                "content": chunk.get("content", ""),
                                "step_id": step_id,
                                "agent_name": agent_name,
                                "timestamp": datetime.now().isoformat(),
                            }
                            self.captured_retrieved_context.append(context_entry)
        except Exception as e:
            console.print(f"[yellow]Warning extracting vector context: {e}[/yellow]")

    def _extract_output_content(self, output: str) -> str:
        """Extract only content from tool output, removing metadata.

        Args:
            output: Raw tool output string

        Returns:
            Cleaned output with only content
        """
        try:
            if output.strip().startswith("{") or output.strip().startswith("["):
                try:
                    data = json.loads(output)

                    if isinstance(data, dict):
                        if "chunks" in data and isinstance(data["chunks"], list):
                            contents = []
                            for chunk in data["chunks"][:3]:
                                if isinstance(chunk, dict) and "content" in chunk:
                                    contents.append(chunk["content"])
                            if contents:
                                combined = "\n---\n".join(contents)
                                return combined + "..."

                        if isinstance(data, list):
                            return str(data) + "..."

                    if isinstance(data, list):
                        return str(data) + "..."

                except json.JSONDecodeError:
                    pass

            return output + "..."

        except Exception:
            return output + "..."


    def _extract_retrieved_context_from_tools(self):
        """Extract essential retrieved context from tool panels."""
        try:
            for step_id, panel in self.tool_panels.items():
                tool_name = panel.get("title", "").replace("Tool: ", "")
                chunks = panel.get("chunks", [])

                if chunks:
                    full_output = "".join(chunks)

                    self.captured_retrieved_context.append(
                        {
                            "type": "tool_panel_output",
                            "tool_name": tool_name,
                            "content": full_output + "..." if len(full_output) > 1000 else full_output,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                    if full_output.strip().startswith("{") or full_output.strip().startswith("["):
                        try:
                            parsed_data = json.loads(full_output.strip())
                            self._extract_structured_retrieval_data(parsed_data, tool_name)
                        except json.JSONDecodeError:
                            pass

        except Exception as e:
            console.print(f"[yellow]Warning extracting context from tool panels: {e}[/yellow]")

    def _extract_retrieval_data_from_output(self, output: str, tool_name: str):
        """Extract essential retrieval information from tool output.

        Args:
            output: Tool output text
            tool_name: Name of the tool
        """
        try:
            self.captured_retrieved_context.append(
                {
                    "type": "retrieval_raw",
                    "tool_name": tool_name,
                    "raw_output": output + "..." if len(output) > 1000 else output,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            if output.strip().startswith("{") or output.strip().startswith("["):
                try:
                    output_data = json.loads(output.strip())
                    self._extract_structured_retrieval_data(output_data, tool_name)
                except json.JSONDecodeError:
                    pass

        except Exception as e:
            self.captured_retrieved_context.append(
                {"parsing_error": str(e), "tool_name": tool_name, "type": "retrieval_error"}
            )

    def _extract_structured_retrieval_data(self, data: Any, tool_name: str):
        """Extract essential structured retrieval data from parsed JSON.

        Args:
            data: Parsed JSON data
            tool_name: Name of the tool
        """
        try:
            if isinstance(data, dict):
                context_fields = ["context", "chunks", "results", "documents", "content", "data"]
                for field in context_fields:
                    if field in data:
                        chunks = data[field]
                        if isinstance(chunks, list):
                            for i, chunk in enumerate(chunks):
                                if isinstance(chunk, dict):
                                    chunk_content = chunk.get("content", chunk.get("text", ""))
                                    chunk_data = {
                                        "type": "retrieval_chunk",
                                        "tool_name": tool_name,
                                        "chunk_index": i,
                                        "content": chunk_content + "..." if len(chunk_content) > 500 else chunk_content,
                                        "timestamp": datetime.now().isoformat(),
                                    }
                                    self.captured_retrieved_context.append(chunk_data)

                                    formatted_content = f"[Chunk {i + 1} from {tool_name}] {chunk_data['content']}"
                                    if chunk_data["content"] and formatted_content not in self.captured_sources:
                                        self.captured_sources.append(formatted_content)

                                elif isinstance(chunk, str):
                                    self.captured_retrieved_context.append(
                                        {
                                            "type": "retrieval_text",
                                            "tool_name": tool_name,
                                            "content": chunk + "..." if len(chunk) > 500 else chunk,
                                            "timestamp": datetime.now().isoformat(),
                                        }
                                    )
                        break

        except Exception as e:
            self.captured_retrieved_context.append(
                {"parsing_error": str(e), "tool_name": tool_name, "type": "structured_extraction_error"}
            )

    def capture_error_data(self, error: Exception, error_context: str = ""):
        """Capture essential error data when SDK calls fail.

        Args:
            error: Exception that occurred
            error_context: Additional context about the error
        """
        try:
            self.error_occurred = True
            self.error_details = {
                "error_type": type(error).__name__,
                "error_message": str(error),
                "error_context": error_context,
                "timestamp": datetime.now().isoformat(),
            }

            self.captured_trajectory.append(
                {
                    "step_type": "error",
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                    "error_context": error_context,
                    "timestamp": datetime.now().isoformat(),
                    "relative_time": time.time() - self.start_time,
                }
            )

            self.captured_retrieved_context.append(
                {
                    "type": "error_context",
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                    "error_context": error_context,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            error_source = f"[Error: {type(error).__name__}] {str(error)}"
            if error_source not in self.captured_sources:
                self.captured_sources.append(error_source)

            self.captured_tool_executions.append(
                {
                    "tool_name": "error_handler",
                    "arguments": {"error_context": error_context},
                    "output": str(error),
                    "status": "failed",
                    "duration_ms": 0,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            error_thinking = self._create_thinking_data(content=f"Error occurred: {str(error)}", kind="error_thinking")
            self.captured_thinking_steps.append(error_thinking)

        except Exception as e:
            console.print(f"[yellow]Warning capturing error data: {e}[/yellow]")

    def get_formatted_sources(self) -> str:
        """Get tool query/output and reference chunks used by the agent.

        Returns:
            Formatted string with all sources
        """
        all_sources = []
        separator = "\n\n" + "=" * 50 + "\n"

        tool_sources = [s for s in self.captured_sources if s.startswith("[Tool:")]
        if tool_sources:
            all_sources.extend(tool_sources)

        if self.captured_retrieved_context:
            reference_chunks = []
            for ctx in self.captured_retrieved_context:
                if isinstance(ctx, dict) and ctx.get("type") == "final_response_reference":
                    i = ctx.get("reference_index", 0)
                    title = ctx.get("title", "")
                    source = ctx.get("source", "")
                    content = ctx.get("content", "")

                    if content:
                        header = (
                            f"[Reference {i + 1}]"
                            + (f" {title}" if title else "")
                            + (f" from {source}" if source else "")
                        )
                        reference_chunks.append(f"{header}\n{content}")

            if reference_chunks:
                all_sources.extend(reference_chunks)

        if not all_sources:
            return ""

        return separator.join(all_sources)

    def get_comprehensive_response_data(self) -> dict[str, Any]:
        """Get comprehensive response data with all captured information.

        Returns:
            Dictionary with all captured data
        """
        return {
            "final_response": self.final_response,
            "execution_metadata": self.execution_metadata,
            "error_occurred": self.error_occurred,
            "error_details": self.error_details,
            "data_capture_summary": {
                "trajectory_steps": len(self.captured_trajectory),
                "tool_executions": len(self.captured_tool_executions),
                "retrieved_context_items": len(self.captured_retrieved_context),
                "sources_count": len(self.captured_sources),
                "raw_events_count": len(self.captured_raw_events),
            },
        }
