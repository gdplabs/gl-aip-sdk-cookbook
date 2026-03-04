"""Async Event Processor for arun_agent SSE events.

This module provides an event processor for capturing agent execution data
from the async streaming arun_agent interface.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import time
from datetime import datetime
from typing import Any


class AsyncEventProcessor:
    """Process SSE events from arun_agent and capture execution data."""

    def __init__(self):
        """Initialize event processor."""
        self.captured_tool_executions = []
        self.captured_retrieved_context = []
        self.captured_thinking_steps = []
        self.captured_sources = []
        self.captured_trajectory = []
        self.captured_raw_events = []
        self.captured_artifacts = []
        self.final_response = ""
        self.response_tokens = []
        self.tool_panels = {}
        self.current_tool = None
        self.tool_start_times = {}
        self.start_time = time.time()
        self.execution_metadata = {}
        self.error_occurred = False
        self.error_details = {}
        self.total_usage = {}

    def process_event(self, event: dict[str, Any]) -> None:
        """Process a single SSE event from arun_agent.

        Args:
            event: Event dict from arun_agent iterator (already parsed from SSE)
        """
        try:
            current_time = time.time()
            relative_time = current_time - self.start_time
            metadata = event.get("metadata", {})
            kind = metadata.get("kind", "")
            content = event.get("content", "")

            event_copy = {"timestamp": current_time, "relative_time": relative_time, "event_data": event.copy()}
            self.captured_raw_events.append(event_copy)

            self._process_thinking_event(event, kind, content, current_time, relative_time)
            self._process_tool_event(event, kind, metadata, current_time, relative_time)
            self._process_references_event(event, kind, metadata)
            self._process_response_event(event, kind, content)
            self._process_artifacts_event(event, current_time)

        except Exception as e:
            error_event = {
                "timestamp": time.time(),
                "error": str(e),
                "original_event": event.get("metadata", {}).get("kind", "unknown"),
            }
            self.captured_raw_events.append(error_event)

    def _process_thinking_event(
        self, event: dict, kind: str, content: str, current_time: float, relative_time: float
    ) -> None:
        """Process thinking/reasoning events.

        Args:
            event: Event dictionary from arun_agent
            kind: Event kind from metadata
            content: Event content text
            current_time: Current timestamp
            relative_time: Time relative to start
        """
        thinking_kinds = ["agent_thinking_step", "final_agent_thinking_step", "thinking", "reasoning"]

        if kind in thinking_kinds and content:
            metadata = event.get("metadata", {})

            thinking_data = {
                "timestamp": datetime.fromtimestamp(current_time).isoformat(),
                "content": content,
                "kind": kind,
                "relative_time": relative_time,
                "step_id": metadata.get("step_id", ""),
                "agent_name": metadata.get("agent_name", ""),
            }

            activity_info = metadata.get("thinking_and_activity_info", {})
            if activity_info and activity_info.get("data_type") == "activity":
                tool_info = metadata.get("tool_info", {})
                tool_calls = tool_info.get("tool_calls", [])

                delegation_calls = [tc for tc in tool_calls if "delegate_to" in tc.get("name", "")]

                if delegation_calls:
                    thinking_data["is_delegation"] = True
                    thinking_data["delegating_to"] = [tc["name"] for tc in delegation_calls]
                    thinking_data["delegation_queries"] = [
                        tc.get("args", {}).get("query", "") for tc in delegation_calls
                    ]

            self.captured_thinking_steps.append(thinking_data)

    def _process_tool_event(
        self, event: dict, kind: str, metadata: dict, current_time: float, relative_time: float
    ) -> None:
        """Process tool execution events from agent_thinking_step metadata.tool_info.

        Args:
            event: Event dictionary from arun_agent
            kind: Event kind from metadata
            metadata: Event metadata dictionary
            current_time: Current timestamp
            relative_time: Time relative to start
        """
        if "tool_info" not in metadata or kind != "agent_thinking_step":
            return

        tool_info = metadata.get("tool_info", {})
        if not isinstance(tool_info, dict) or not tool_info:
            return

        if "tool_calls" in tool_info and isinstance(tool_info.get("tool_calls"), list):
            self._process_tool_calls(tool_info["tool_calls"], metadata, current_time)
            return

        if "name" in tool_info and "output" in tool_info:
            self._process_tool_completion(tool_info, metadata, current_time)

    def _process_tool_calls(self, tool_calls: list[dict], metadata: dict, current_time: float) -> None:
        """Process tool call events.

        Args:
            tool_calls: List of tool call dictionaries from tool_info
            metadata: Event metadata dictionary
            current_time: Current timestamp
        """
        for tool_call in tool_calls:
            tool_id = tool_call.get("id", f"tool_{len(self.tool_panels)}")
            tool_name = tool_call.get("name", "unknown")

            self.tool_start_times[tool_id] = current_time
            self.tool_panels[tool_id] = {
                "tool_name": tool_name,
                "arguments": tool_call.get("args", {}),
                "tool_id": tool_id,
                "start_time": current_time,
            }

            if "delegate_to_" in tool_name:
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
                }
                self.captured_tool_executions.append(delegation_start)

    def _process_tool_completion(self, tool_info: dict, metadata: dict, current_time: float) -> None:
        """Process tool completion events.

        Args:
            tool_info: Tool information dictionary from metadata
            metadata: Event metadata dictionary
            current_time: Current timestamp
        """
        tool_id = tool_info.get("id", f"tool_{len(self.captured_tool_executions)}")
        execution_time_s = tool_info.get("execution_time", 0)
        duration_ms = int(execution_time_s * 1000) if execution_time_s else 0

        tool_name = tool_info.get("name", "unknown")
        is_delegation = "delegate_to_" in tool_name

        tool_execution = {
            "tool_name": tool_name,
            "arguments": tool_info.get("args", {}),
            "output": tool_info.get("output", ""),
            "status": "delegation_complete" if is_delegation else "finished",
            "duration_ms": duration_ms,
            "step_id": metadata.get("step_id", tool_id),
            "tool_id": tool_id,
            "agent_name": metadata.get("agent_name", ""),
            "previous_step_ids": metadata.get("previous_step_ids", []),
        }

        self.captured_tool_executions.append(tool_execution)
        self.tool_panels[tool_id] = tool_execution

    def _process_references_event(self, event: dict, kind: str, metadata: dict) -> None:
        """Process references/context from final_response.

        Args:
            event: Event dictionary from arun_agent
            kind: Event kind from metadata
            metadata: Event metadata dictionary
        """
        if kind != "final_response":
            return

        references = metadata.get("references", [])
        for i, ref in enumerate(references):
            if not ref:
                continue

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
                formatted = self._format_reference(essential_ref, i)
                if formatted not in self.captured_sources:
                    self.captured_sources.append(formatted)

    def _format_reference(self, ref: dict, index: int) -> str:
        """Format reference for display.

        Args:
            ref: Reference dictionary with title, source, content
            index: Reference index number

        Returns:
            Formatted reference string with header and content
        """
        title = ref["title"]
        source = ref["source"]
        header = f"[Reference {index + 1}]"
        if title:
            header += f" {title}"
        if source:
            header += f" from {source}"
        return f"{header}\n{ref['content']}"

    def _process_response_event(self, event: dict, kind: str, content: str) -> None:
        """Process response text events.

        Args:
            event: Event dictionary from arun_agent
            kind: Event kind from metadata
            content: Event content text
        """
        if kind == "token" or kind == "text":
            if content:
                self.response_tokens.append(content)

        if kind == "final_response" or kind == "completed":
            final_content = event.get("content", event.get("output", ""))
            if final_content:
                self.final_response = final_content

            metadata = event.get("metadata", {})
            total_usage = metadata.get("total_usage", {})
            if total_usage:
                self.total_usage = total_usage

    def _process_artifacts_event(self, event: dict, current_time: float) -> None:
        """Process artifacts from e2b_sandbox_tool (file generations).

        Args:
            event: Event dictionary from arun_agent
            current_time: Current timestamp
        """
        artifacts = event.get("artifacts", [])
        if not artifacts:
            return

        for artifact in artifacts:
            artifact_data = {
                "artifact_id": artifact.get("artifact_id", ""),
                "name": artifact.get("name", ""),
                "file_name": artifact.get("file_name", ""),
                "content_type": artifact.get("content_type", ""),
                "mime_type": artifact.get("mime_type", ""),
                "file_uri": artifact.get("file_uri", ""),
                "has_file_data": artifact.get("has_file_data", False),
                "timestamp": datetime.fromtimestamp(current_time).isoformat(),
            }
            self.captured_artifacts.append(artifact_data)

    def finalize(self) -> None:
        """Finalize processing after all events received."""
        if not self.final_response and self.response_tokens:
            self.final_response = "".join(self.response_tokens)

        if not self.captured_tool_executions and self.tool_panels:
            for step_id, tool_data in self.tool_panels.items():
                self.captured_tool_executions.append(tool_data.copy())

        self.execution_metadata = {
            "duration_s": time.time() - self.start_time,
            "finished_at": time.time(),
            "total_events": len(self.captured_raw_events),
            "thinking_steps_count": len(self.captured_thinking_steps),
            "tool_executions_count": len(self.captured_tool_executions),
            "retrieved_context_count": len(self.captured_retrieved_context),
        }

    def get_comprehensive_response_data(self) -> dict[str, Any]:
        """Get all captured data in a structured format.

        Returns:
            Dictionary with all captured execution data
        """
        return {
            "response": self.final_response,
            "tool_executions": self.captured_tool_executions,
            "retrieved_context": self.captured_retrieved_context,
            "thinking_steps": self.captured_thinking_steps,
            "sources": self.captured_sources,
            "trajectory": self.captured_trajectory,
            "artifacts": self.captured_artifacts,
            "metadata": self.execution_metadata,
            "error_occurred": self.error_occurred,
            "error_details": self.error_details,
            "total_usage": self.total_usage,
        }

    def get_formatted_sources(self) -> str:
        """Get formatted source texts.

        Returns:
            Formatted string with all sources separated by separator
        """
        if not self.captured_sources:
            return ""
        
        separator = "\n\n" + "=" * 50 + "\n"
        return separator.join(self.captured_sources)
