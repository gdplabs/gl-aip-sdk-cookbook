"""GLAIP Agent Benchmark - Main Entry Point.

A modular, clean benchmark system for evaluating GLAIP SDK agents.
This refactored version provides better code organization and maintainability.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import argparse
import asyncio
import csv
import os
import sys
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables from .env file (if it exists)
# This allows setting defaults without needing to export them each time
load_dotenv()

# Increase CSV field size limit to handle large agent responses and trajectories
csv.field_size_limit(10 * 1024 * 1024)  # 10MB limit

sys.path.insert(0, os.path.dirname(__file__))

from components import BenchmarkConfig, ComprehensiveAgentEvaluator, CSVHandler

console = Console()


def parse_row_indices(rows_str: str) -> list[int] | None:
    """Parse row indices from string format.
    
    Supports formats:
    - Single numbers: '1,3,5' -> [1, 3, 5]
    - Ranges: '1-5' -> [1, 2, 3, 4, 5]
    - Mixed: '1,3-5,10' -> [1, 3, 4, 5, 10]
    
    Args:
        rows_str: String containing row numbers
        
    Returns:
        List of row indices (1-based), or None if empty
    """
    if not rows_str:
        return None
    
    indices = []
    parts = rows_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = part.split('-')
                start_idx = int(start.strip())
                end_idx = int(end.strip())
                indices.extend(range(start_idx, end_idx + 1))
            except ValueError:
                console.print(f"[yellow]Warning: Invalid range '{part}', skipping[/yellow]")
        else:
            try:
                indices.append(int(part))
            except ValueError:
                console.print(f"[yellow]Warning: Invalid number '{part}', skipping[/yellow]")
    
    return sorted(set(indices)) if indices else None


def prepare_dataset_from_df(df: pd.DataFrame, column_mapping: dict[str, str]) -> list[dict[str, Any]]:
    """Convert DataFrame to dataset format for gllm_evals.evaluate().
    
    Args:
        df: DataFrame with questions
        column_mapping: Column name mapping
    
    Returns:
        List of dictionaries in gllm-evals format
    """
    dataset = []
    for idx, row in df.iterrows():
        question = row[column_mapping["question"]]
        expected_answer = row[column_mapping["expected_answer"]] if "expected_answer" in column_mapping else ""
        requires_visualization = (
            row[column_mapping["requires_visualization"]] if "requires_visualization" in column_mapping else False
        )
        
        dataset.append({
            "query": question,
            "expected_response": expected_answer,
            "requires_visualization": requires_visualization,
            "_original_idx": idx,
        })
    
    return dataset


def _print_benchmark_config(config: BenchmarkConfig):
    """Print benchmark configuration.
    
    Args:
        config: BenchmarkConfig with all settings
    """
    console.print("🚀 Starting GLAIP Agent Benchmark Evaluation")
    console.print(f"   Input: {config.input_file}")
    console.print(f"   Output: {config.output_file}")
    console.print(f"   Agent ID: {config.agent_id}")
    console.print(f"   Limit: {config.limit}")
    console.print(f"   Workers: {config.workers}")
    console.print(f"   Evaluation Model: {config.evaluation_model}")
    console.print(
        f"   Execution Mode: {'arun_agent (native async)' if config.use_arun else 'run_agent (renderer-based)'}"
    )
    console.print(f"   Manual Review Auto Eval Mode: {config.manual_review_auto_eval}")
    console.print("   Using gllm-evals.evaluate() with built-in concurrency")


def _print_benchmark_summary(df, results: list[dict[str, Any]], config: BenchmarkConfig):
    """Print benchmark execution summary.
    
    Args:
        df: Original dataset DataFrame
        results: List of result dictionaries
        config: BenchmarkConfig with all settings
    """
    console.print(f"\n{'=' * 50}")
    console.print("📊 Benchmark Summary")
    console.print(f"   Total Questions: {len(df)}")
    console.print(f"   Completed: {len(results)}")
    console.print(f"   Output File: {config.output_file}")

    if results:
        avg_response_time = sum(r.get("Response_Time", 0) for r in results) / len(results)
        console.print(f"   Average Response Time: {avg_response_time:.2f}s")

        completeness_scores = [
            r.get("geval_completeness") for r in results if r.get("geval_completeness") is not None
        ]
        if completeness_scores:
            avg_completeness = sum(completeness_scores) / len(completeness_scores)
            console.print(f"   Average Completeness: {avg_completeness:.2f}/5")

        auto_rr_values = [r.get("auto_rr") for r in results if r.get("auto_rr")]
        if auto_rr_values:
            from collections import Counter

            rr_dist = Counter(auto_rr_values)
            console.print(f"   auto_rr distribution: {dict(rr_dist)}")

    console.print("\n✅ Benchmark complete!")


async def _run_evaluation_with_gllm_evals(
    evaluator,
    dataset: list[dict[str, Any]],
    config: BenchmarkConfig,
) -> list[dict[str, Any]]:
    """Run evaluation using gllm-evals.evaluate().
    
    Args:
        evaluator: ComprehensiveAgentEvaluator instance
        dataset: Prepared dataset for evaluation
        config: BenchmarkConfig with all settings
        
    Returns:
        List of result dictionaries
    """
    from gllm_evals import evaluate
    from gllm_evals.dataset import DictDataset
    import os
    import pandas as pd
    import logging
    import traceback
    
    evaluators_list = evaluator.get_evaluators()
    inference_fn = evaluator.create_inference_fn()
    
    # Set environment variables for gllm-evals timeout configuration
    os.environ["GLLM_EVALS_TIMEOUT"] = "600"  # 10 minute timeout
    os.environ["GLLM_EVALS_MAX_RETRIES"] = "6"  # Max retries
    os.environ["GLLM_EVALS_MAX_BACKOFF"] = "60"  # Max backoff in seconds
    
    console.print(f"\n🚀 Starting evaluation with gllm-evals")
    console.print(f"   Batch size: {config.workers}")
    console.print(f"   Max row concurrency: {config.workers}")
    console.print(f"   Timeout config: 600s, max_retries: 6")
    
    # Wrap dataset in DictDataset for gllm-evals
    dict_dataset = DictDataset(dataset, dataset_name="benchmark_dataset")
    
    # Use gllm-evals.evaluate() with proper concurrency settings
    evaluation_result = await evaluate(
        data=dict_dataset,
        inference_fn=inference_fn,
        evaluators=evaluators_list,
        batch_size=config.workers,  # Runner-level chunking
        max_row_concurrency=config.workers,  # Concurrent inference calls
        show_results=True,  # Get detailed results
        output_dir="./benchmark_experiments",  # Specify output directory for experiment tracker
    )
    
    # Extract results from experiment tracker CSV
    console.print(f"\n✅ Evaluation complete!")
    console.print(f"📊 Run ID: {evaluation_result.get('run_id')}")
    
    # Setup detailed logging to file
    log_file = f"geval_debug_{evaluation_result.get('run_id', 'unknown')}.log"
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger('geval_debug')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    logger.info(f"=== GEval Debug Log for run_id: {evaluation_result.get('run_id')} ===")
    
    if "results" in evaluation_result and evaluation_result["results"]:
        console.print(f"📊 Found {len(evaluation_result['results'])} result sets in evaluation_result")
        logger.info(f"Found {len(evaluation_result['results'])} result sets")
        
        for i, result_set in enumerate(evaluation_result["results"][:1]):  # Show first result
            console.print(f"   Result set {i}: {type(result_set)} with {len(result_set) if isinstance(result_set, list) else 'N/A'} items")
            logger.info(f"Result set {i}: {type(result_set)} with {len(result_set) if isinstance(result_set, list) else 'N/A'} items")
            
            if isinstance(result_set, list):
                for j, item in enumerate(result_set):
                    console.print(f"     Item {j} type: {type(item).__name__}")
                    logger.info(f"  Item {j} type: {type(item).__name__}")
                    
                    if isinstance(item, dict):
                        console.print(f"       Keys: {list(item.keys())}")
                        logger.info(f"    Keys: {list(item.keys())}")
                        logger.debug(f"    Full item {j} dict: {item}")
                    elif isinstance(item, Exception):
                        error_str = str(item)
                        console.print(f"       Exception: {error_str[:200]}")
                        logger.error(f"    Exception on item {j}: {error_str}")
                        logger.error(f"    Exception type: {type(item).__name__}")
                        logger.error(f"    Exception args: {item.args}")
                        if hasattr(item, '__traceback__'):
                            tb_lines = traceback.format_tb(item.__traceback__)
                            logger.error(f"    Traceback:\n{''.join(tb_lines)}")
                    else:
                        console.print(f"       Value: {str(item)[:200]}")
                        logger.info(f"    Value: {str(item)[:200]}")
    
    logger.info(f"Log saved to: {log_file}")
    console.print(f"📝 Detailed debug log saved to: {log_file}")
    
    console.print(f"📊 Reading results from experiment tracker...")
    
    experiment_csv = "./benchmark_experiments/experiment_results.csv"
    
    try:
        # Read experiment results CSV which has both inference and evaluation data
        df_results = pd.read_csv(experiment_csv)
        
        # Filter by this run_id
        run_id = evaluation_result.get('run_id')
        if run_id:
            df_results = df_results[df_results['run_id'] == run_id]
        
        console.print(f"📊 Found {len(df_results)} results in experiment tracker")
        
        # Extract GEval scores from evaluation_result["results"]
        geval_scores = []
        if "results" in evaluation_result and evaluation_result["results"]:
            for result_set in evaluation_result["results"]:
                if isinstance(result_set, list):
                    # Find the generation evaluator results (dict with 'generation' key)
                    geval_data = None
                    for item in result_set:
                        if isinstance(item, dict) and 'generation' in item:
                            geval_data = item['generation']
                            break
                    geval_scores.append(geval_data)
                else:
                    geval_scores.append(None)
        
        logger.info(f"Extracted {len(geval_scores)} GEval score sets")
        
        # Convert experiment tracker results to our CSV format
        results = CSVHandler.convert_experiment_tracker_results(
            df_results=df_results,
            manual_review_auto_eval=config.manual_review_auto_eval,
            geval_scores=geval_scores,
        )
        return results
    except Exception as e:
        console.print(f"[yellow]⚠️  Error reading experiment results: {e}[/yellow]")
        console.print(f"[yellow]Traceback: {traceback.format_exc()}[/yellow]")
        return []


async def _run_without_evaluation(
    dataset: list[dict[str, Any]],
    evaluator,
    config: BenchmarkConfig,
) -> list[dict[str, Any]]:
    """Run agent inference without evaluation.
    
    Args:
        dataset: Prepared dataset
        evaluator: ComprehensiveAgentEvaluator instance
        config: BenchmarkConfig with all settings
        
    Returns:
        List of result dictionaries
    """
    console.print(f"\n🚀 Starting execution without evaluation")
    console.print(f"   Workers: {config.workers}")
    console.print(f"   Concurrency: {'Enabled' if config.workers > 1 else 'Sequential'}")
    
    inference_fn = evaluator.create_inference_fn()
    
    async def run_inference(idx: int, data_item: dict[str, Any]) -> tuple[int, dict[str, Any], dict[str, Any]]:
        """Run inference for a single data item."""
        console.print(f"\n{'=' * 50}")
        console.print(f"📝 Processing Question {idx + 1}/{len(dataset)}")
        
        # Run inference only
        enriched_data = await inference_fn(data_item)
        
        console.print(f"✅ Completed Question {idx + 1}")
        return (idx, data_item, enriched_data)
    
    # First pass: Run all inference to collect results
    inference_results = []
    
    if config.workers > 1:
        # Process in batches to respect worker limit
        for i in range(0, len(dataset), config.workers):
            batch = dataset[i:i + config.workers]
            batch_tasks = [
                run_inference(i + j, data_item)
                for j, data_item in enumerate(batch)
            ]
            batch_results = await asyncio.gather(*batch_tasks)
            inference_results.extend(batch_results)
    else:
        # Sequential execution
        for idx, data_item in enumerate(dataset):
            result = await run_inference(idx, data_item)
            inference_results.append(result)
    
    # Calculate max_tools across all results
    max_tools = 0
    for _, _, enriched_data in inference_results:
        metadata = enriched_data.get("_metadata", {})
        step_timings = metadata.get("step_timings", [])
        finished_tools = [t for t in step_timings if t.get("status") in ("finished", "delegation_complete")]
        max_tools = max(max_tools, len(finished_tools))
    
    console.print(f"📊 Max tools found across all rows: {max_tools}")
    
    # Second pass: Build result rows with consistent max_tools
    results = []
    for idx, data_item, enriched_data in inference_results:
        result_row = CSVHandler.build_result_row_from_inference(
            idx=idx,
            data_item=data_item,
            enriched_data=enriched_data,
            manual_review_auto_eval=config.manual_review_auto_eval,
            max_tools=max(max_tools, 1),  # At least 1 tool column
        )
        results.append(result_row)
    
    return results


async def process_benchmark_dataset(config: BenchmarkConfig):
    """Process a benchmark dataset using gllm_evals.evaluate().

    Args:
        config: BenchmarkConfig with all settings
    """
    _print_benchmark_config(config)

    df = CSVHandler.load_dataset(config.input_file, config.limit, config.questions, config.row_indices)
    column_mapping = CSVHandler.get_column_mapping(df)

    evaluator = ComprehensiveAgentEvaluator(config)
    
    # Prepare dataset for gllm-evals
    dataset = prepare_dataset_from_df(df, column_mapping)
    
    # Get evaluators
    evaluators_list = evaluator.get_evaluators()
    if not evaluators_list:
        console.print("[yellow]⚠️  No evaluators available. Running agent only without evaluation.[/yellow]")
    
    # Run evaluation or inference-only
    if evaluators_list:
        results = await _run_evaluation_with_gllm_evals(evaluator, dataset, config)
    else:
        results = await _run_without_evaluation(dataset, evaluator, config)

    CSVHandler.save_results(results, config.output_file)
    _print_benchmark_summary(df, results, config)


def main():
    """Main entry point for the benchmark CLI."""
    parser = argparse.ArgumentParser(
        description="GLAIP Agent Benchmark - Evaluate agent performance with comprehensive metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run benchmark on first 10 questions
  python benchmark.py --input input.csv --agent-id <AGENT_ID> --limit 10

  # Run with parallel workers
  python benchmark.py --input input.csv --agent-id <AGENT_ID> --workers 5

  # Use arun_agent (native async) instead of run_agent
  python benchmark.py --input input.csv --agent-id <AGENT_ID> --use-arun

  # Specify custom output file
  python benchmark.py --input input.csv --agent-id <AGENT_ID> --output results.csv
        """,
    )

    parser.add_argument("--input", "-i", required=True, help="Input CSV file with questions")
    parser.add_argument("--agent-id", required=True, help="GLAIP Agent ID to evaluate")

    parser.add_argument("--output", "-o", help="Output CSV file for results (default: auto-generated with timestamp)")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of questions to process")
    parser.add_argument("--questions", nargs="+", help="Specific questions to process")
    parser.add_argument("--rows", "-r", type=str, help="Specific row numbers to process (e.g., '1,3,5' or '1-5' or '1,3-5,10')")
    parser.add_argument("--openai-key", help="OpenAI API key for evaluation (or set OPENAI_API_KEY env var)")
    parser.add_argument("--evaluation-model", default="gpt-4o-mini", help="Model to use for evaluation")
    parser.add_argument("--agent-timeout", type=float, default=600.0, help="Agent execution timeout in seconds (default: 600)")
    parser.add_argument("--backoff", type=float, default=15.0, help="Backoff time between requests in seconds (default: 15.0)")
    parser.add_argument("--max-retry-duration", type=float, default=300.0, help="Maximum total time to spend retrying in seconds (default: 300)")
    parser.add_argument("--workers", "-w", type=int, default=1, help="Number of parallel workers (default: 1)")
    parser.add_argument("--use-arun", action="store_true", help="Use arun_agent (native async) instead of run_agent")
    parser.add_argument(
        "--manual-review-auto-eval",
        action="store_true",
        help="Use detailed manual review columns (manual_rr, manual_completeness, manual_redundancy, manual_groundedness) instead of simplified columns (manual_rr, issue_category, additional_notes)",
    )

    args = parser.parse_args()
    
    # Parse row indices if provided
    row_indices = parse_row_indices(args.rows) if args.rows else None

    openai_api_key = args.openai_key or os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        console.print("[yellow]⚠️  OpenAI API key not provided. Evaluation metrics will not be available.[/yellow]")

    try:
        config = BenchmarkConfig(
            agent_id=args.agent_id,
            agent_timeout=args.agent_timeout,
            use_arun=args.use_arun,
            backoff_time=args.backoff,
            max_retry_duration=args.max_retry_duration,
            manual_review_auto_eval=args.manual_review_auto_eval,
            openai_api_key=openai_api_key,
            evaluation_model=args.evaluation_model,
            workers=args.workers,
            limit=args.limit,
            questions=args.questions,
            row_indices=row_indices,
            input_file=args.input,
            output_file=args.output,
        )
    except ValueError as e:
        console.print(f"[red]❌ Configuration error: {e}[/red]")
        sys.exit(1)

    try:
        asyncio.run(process_benchmark_dataset(config))
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Benchmark interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Benchmark failed: {e}[/red]")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
