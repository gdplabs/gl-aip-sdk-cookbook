"""Agent evaluator for running and evaluating agent queries.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import asyncio
import json
import os
import sys
import time
from typing import Any

from glaip_sdk import Client
from rich.console import Console

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from .artifact_metric import ArtifactValidationMetric
import inspect

from ..config import BenchmarkConfig
from ..capture.renderer import OptimizedCLIAgentRenderer

from ..capture import AsyncEventProcessor

console = Console()



class ComprehensiveAgentEvaluator:
    """Evaluator for comprehensive agent benchmarking and evaluation.
    
    This class now works with gllm-evals.evaluate() by providing an inference function
    that runs the agent and returns enriched data with artifacts and metadata.
    """

    def __init__(self, config: BenchmarkConfig):
        """Initialize the comprehensive agent evaluator.

        Args:
            config: BenchmarkConfig instance with all settings
        """
        self.agent_id = config.agent_id
        self.openai_api_key = config.openai_api_key
        self.evaluation_model = config.evaluation_model
        self.agent_timeout = config.agent_timeout
        self.use_arun = config.use_arun

        self.client = Client(api_url=config.api_url, api_key=config.api_key, timeout=self.agent_timeout)
        console.print("✅ GLAIP SDK client initialized successfully")

    async def run_agent_query(self, question: str) -> dict[str, Any]:
        """Execute agent query and capture comprehensive execution data.

        Args:
            question: Question to ask the agent

        Returns:
            Dictionary containing response, trajectory, context, sources, and timing data
        """
        if self.use_arun:
            return await self._run_agent_query_arun(question)
        else:
            return await self._run_agent_query_renderer(question)

    def _handle_agent_error(
        self, error: Exception, renderer_or_processor, execution_time: float
    ) -> dict[str, Any]:
        """Handle agent execution errors and capture comprehensive debug data.
        
        Args:
            error: The exception that occurred
            renderer_or_processor: The renderer (OptimizedCLIAgentRenderer) or processor (AsyncEventProcessor)
            execution_time: Actual execution time before error
            
        Returns:
            Dictionary with error data and captured state
        """
        error_type = (
            "TIMEOUT"
            if "timeout" in str(error).lower() or "timed out" in str(error).lower()
            else "SDK_ERROR"
        )
        error_name = type(error).__name__
        error_msg = str(error)

        console.print(f"❌ SDK error: {error_name}: {error_msg[:200]}")
        console.print(f"🔍 Debugging {error_type} - captured state:")
        console.print(f"   Error Type: {error_name}")
        console.print(f"   Tool executions: {len(renderer_or_processor.captured_tool_executions)}")
        console.print(f"   Trajectory steps: {len(renderer_or_processor.captured_trajectory)}")
        console.print(f"   Thinking steps: {len(renderer_or_processor.captured_thinking_steps)}")
        console.print(f"   Raw events: {len(renderer_or_processor.captured_raw_events)}")

        if renderer_or_processor.captured_tool_executions:
            console.print("\n📋 Last tool executions before error:")
            for i, tool in enumerate(renderer_or_processor.captured_tool_executions[-3:], 1):
                console.print(
                    f"   {i}. {tool.get('tool_name', 'unknown')} - {tool.get('status', 'unknown')} - {tool.get('duration_ms', 0)}ms"
                )

        if renderer_or_processor.captured_thinking_steps:
            console.print("\n💭 Last thinking steps before error:")
            for i, step in enumerate(renderer_or_processor.captured_thinking_steps[-3:], 1):
                content = step.get("content", "")[:100]
                console.print(f"   {i}. {step.get('kind', 'unknown')}: {content}...")

        error_details = {
            "error_type": error_type,
            "error_class": error_name,
            "error_message": error_msg[:500],
            "timeout_seconds": self.agent_timeout,
            "actual_duration": execution_time,
            "tools_executed": len(renderer_or_processor.captured_tool_executions),
            "last_tools": [t.get("tool_name", "unknown") for t in renderer_or_processor.captured_tool_executions[-5:]],
            "trajectory_steps": len(renderer_or_processor.captured_trajectory),
            "thinking_steps": len(renderer_or_processor.captured_thinking_steps),
            "raw_events_count": len(renderer_or_processor.captured_raw_events),
        }

        full_error_msg = f"{error_name}: {error_msg}. Debug info: {json.dumps(error_details, indent=2)}"
        console.print("❌ Full error details captured for CSV output")

        # Capture error data in renderer/processor if it has the method
        if hasattr(renderer_or_processor, 'capture_error_data'):
            renderer_or_processor.capture_error_data(error, f"SDK execution failed for agent {self.agent_id}")

        return {
            "response": f"{error_name}: {error_msg}",
            "execution_time": execution_time,
            "trajectory": renderer_or_processor.captured_trajectory,
            "step_timings": renderer_or_processor.captured_tool_executions,
            "retrieved_context": renderer_or_processor.captured_retrieved_context,
            "sources": renderer_or_processor.get_formatted_sources(),
            "thinking_steps": renderer_or_processor.captured_thinking_steps,
            "raw_events": renderer_or_processor.captured_raw_events,
            "complete_response_data": renderer_or_processor.get_comprehensive_response_data(),
            "error": full_error_msg,
        }

    async def _run_agent_query_renderer(self, question: str) -> dict[str, Any]:
        """Execute agent query using run_agent with renderer (thread-based)."""
        console.print(f"🤖 Running agent query via run_agent (renderer): {question[:80]}...")

        start_time = time.time()
        renderer = OptimizedCLIAgentRenderer()

        try:
            console.print(f"🔧 Running agent {self.agent_id} with optimized renderer...")
            console.print(f"⏱️  Timeout set to {self.agent_timeout}s")

            response_text = await asyncio.to_thread(
                self.client.run_agent,
                agent_id=self.agent_id,
                message=question,
                renderer=renderer,
                verbose=True,
                stream=True,
            )

            end_time = time.time()
            execution_time = end_time - start_time

            console.print(f"📄 Response length: {len(response_text)} characters")
            console.print(f"🛠️  Captured {len(renderer.captured_tool_executions)} tool executions")
            console.print(f"📄 Captured {len(renderer.captured_retrieved_context)} context items")
            console.print(f"🔍 Captured {len(renderer.captured_sources)} sources")
            console.print(f"💭 Captured {len(renderer.captured_thinking_steps)} thinking steps")
            console.print(f"📎 Captured {len(renderer.captured_artifacts)} artifacts")

            result = {
                "response": response_text,
                "execution_time": execution_time,
                "trajectory": renderer.captured_trajectory,
                "step_timings": renderer.captured_tool_executions,
                "retrieved_context": renderer.captured_retrieved_context,
                "sources": renderer.get_formatted_sources(),
                "thinking_steps": renderer.captured_thinking_steps,
                "artifacts": renderer.captured_artifacts,
                "error_occurred": False,
                "error": None,
            }
            return result

        except Exception as sdk_error:
            end_time = time.time()
            execution_time = end_time - start_time
            return self._handle_agent_error(sdk_error, renderer, execution_time)

    async def _run_agent_query_arun(self, question: str) -> dict[str, Any]:
        """Execute agent query using arun_agent with AsyncEventProcessor (native async)."""
        console.print(f"🤖 Running agent query via arun_agent (async): {question[:80]}...")

        start_time = time.time()
        processor = AsyncEventProcessor()

        try:
            console.print(f"🔧 Running agent {self.agent_id} with async event processor...")
            console.print(f"⏱️  Timeout set to {self.agent_timeout}s")

            async for event in self.client.agents.arun_agent(
                agent_id=self.agent_id, message=question, timeout=self.agent_timeout
            ):
                processor.process_event(event)

            processor.finalize()

            end_time = time.time()
            execution_time = end_time - start_time

            console.print("✅ Async execution successful")
            console.print(f"📄 Response length: {len(processor.final_response)} characters")
            console.print(f"🛠️  Captured {len(processor.captured_tool_executions)} tool executions")
            console.print(f"📄 Captured {len(processor.captured_retrieved_context)} context items")
            console.print(f"🔍 Captured {len(processor.captured_sources)} sources")
            console.print(f"💭 Captured {len(processor.captured_thinking_steps)} thinking steps")
            console.print(f"📎 Captured {len(processor.captured_artifacts)} artifacts")

            return {
                "response": processor.final_response,
                "execution_time": execution_time,
                "trajectory": processor.captured_trajectory,
                "step_timings": processor.captured_tool_executions,
                "retrieved_context": processor.captured_retrieved_context,
                "sources": processor.get_formatted_sources(),
                "thinking_steps": processor.captured_thinking_steps,
                "artifacts": processor.captured_artifacts,
                "total_usage": processor.total_usage,
                "raw_events": processor.captured_raw_events,
                "complete_response_data": processor.get_comprehensive_response_data(),
                "error": None,
            }

        except Exception as sdk_error:
            end_time = time.time()
            execution_time = end_time - start_time
            processor.finalize()
            processor.error_occurred = True
            return self._handle_agent_error(sdk_error, processor, execution_time)

    def get_evaluators(self) -> list:
        """Get configured evaluators for use with gllm_evals.evaluate().
        
        Returns:
            List of evaluator instances to pass to gllm_evals.evaluate()
        """
        if not (self.openai_api_key):
            console.print("[yellow]Warning: gllm-evals not available or OpenAI API key not provided[/yellow]")
            return []
        
        try:
            # Check available parameters for this version of GEvalGenerationEvaluator
            sig = inspect.signature(GEvalGenerationEvaluator.__init__)
            available_params = set(sig.parameters.keys())
            
            # Build kwargs based on available parameters
            geval_kwargs = {
                "model": f"openai/{self.evaluation_model}",
                "model_credentials": self.openai_api_key,
            }
            
            # Add optional parameters if they exist in this version
            if "run_parallel" in available_params:
                geval_kwargs["run_parallel"] = True
            if "batch_status_check_interval" in available_params:
                geval_kwargs["batch_status_check_interval"] = 60.0
            if "batch_max_iterations" in available_params:
                geval_kwargs["batch_max_iterations"] = 200
            
            console.print(f"🔧 Initializing GEvalGenerationEvaluator with: {list(geval_kwargs.keys())}")
            
            geval_evaluator = GEvalGenerationEvaluator(**geval_kwargs)
            artifact_metric = ArtifactValidationMetric()
            
            evaluators = [geval_evaluator, artifact_metric]
            
            console.print("✅ gllm-evals evaluators initialized successfully")
            console.print(f"   - GEvalGenerationEvaluator: {len(geval_evaluator.metrics)} metrics")
            console.print(f"   - ArtifactValidationMetric: {artifact_metric.name}")
            
            return evaluators
            
        except Exception as e:
            import traceback
            console.print(f"[red]❌ Error initializing gllm-evals evaluators:[/red]")
            console.print(f"[red]   {type(e).__name__}: {e}[/red]")
            console.print(f"[yellow]   Traceback:[/yellow]")
            traceback.print_exc()
            return []
    
    def create_inference_fn(self):
        """Create an inference function for use with gllm_evals.evaluate().
        
        Returns:
            Async function that takes MetricInput and returns enriched data
        """
        async def inference_fn(row: dict[str, Any]) -> dict[str, Any]:
            """Inference function that runs the agent and enriches data.
            
            Args:
                row: Input data containing 'query', 'expected_response', 'requires_visualization', etc.
                     Named 'row' to match gllm-evals InferenceHandler expectations.
            
            Returns:
                Enriched data with agent response, context, artifacts, and metadata
            """
            question = row.get("query", row.get("question", ""))
            
            agent_result = await self.run_agent_query(question)
            
            # Convert retrieved_context to text format for gllm-evals
            # Note: Must be string (not None) for metrics to work properly
            context_text = ""
            if agent_result.get("retrieved_context"):
                context_texts = []
                for ctx in agent_result["retrieved_context"]:
                    if isinstance(ctx, dict):
                        # Handle SQL results
                        if ctx.get("type") == "tool_output_sql_result" and "results" in ctx:
                            results = ctx["results"]
                            if isinstance(results, list) and results:
                                try:
                                    import pandas as pd
                                    df = pd.DataFrame(results)
                                    context_texts.append(f"SQL Results:\n{df.to_markdown(index=False)}")
                                except Exception:
                                    context_texts.append(f"SQL Results:\n{json.dumps(results, ensure_ascii=False)}")
                        # Handle vector chunks
                        elif ctx.get("type") == "vector_chunk" and "content" in ctx:
                            context_texts.append(str(ctx["content"]))
                        # Handle generic content
                        elif "content" in ctx:
                            context_texts.append(str(ctx["content"]))
                    elif isinstance(ctx, str):
                        context_texts.append(ctx)
                context_text = "\n\n".join(context_texts) if context_texts else ""
            
            # Return enriched data with EXACT field names required by gllm-evals metrics
            # Field names MUST match ColumnNames constants in gllm-evals
            enriched_data = {
                # Required fields for all generation metrics
                "query": question,  # ColumnNames.QUERY
                "generated_response": agent_result.get("response", ""),  # ColumnNames.GENERATED_RESPONSE
                "expected_response": row.get("expected_response", row.get("expected_answer", "")),  # ColumnNames.EXPECTED_RESPONSE
                "retrieved_context": context_text,  # ColumnNames.RETRIEVED_CONTEXT (string, not None)
                
                # Additional fields for custom metrics and metadata
                "artifacts": agent_result.get("artifacts", []),
                "requires_visualization": row.get("requires_visualization", False),
                
                # Preserve metadata for CSV output - use .get() to avoid KeyError
                "_metadata": {
                    "execution_time": agent_result.get("execution_time", 0),
                    "trajectory": agent_result.get("trajectory", ""),
                    "step_timings": agent_result.get("step_timings", []),
                    "retrieved_context": agent_result.get("retrieved_context", []),  # Raw list for CSV extraction
                    "thinking_steps": agent_result.get("thinking_steps", []),
                    "sources": agent_result.get("sources", ""),
                    "raw_events": agent_result.get("raw_events", []),
                    "error": agent_result.get("error"),
                },
            }
            
            return enriched_data
        
        return inference_fn
