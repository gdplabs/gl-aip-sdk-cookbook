"""CSV reading and dataset loading functionality.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

from typing import Any

import pandas as pd
from rich.console import Console

console = Console()


def load_dataset(input_file: str, limit: int = None, questions: list[str] = None, row_indices: list[int] = None) -> pd.DataFrame:
    """Load dataset from CSV file.

    Args:
        input_file: Path to input CSV file
        limit: Maximum number of questions to process
        questions: Specific questions to filter by
        row_indices: Specific row indices to process (1-based, matching CSV row numbers)

    Returns:
        DataFrame with loaded data
    """
    try:
        df = pd.read_csv(input_file)
        console.print(f"✅ Loaded {len(df)} questions from {input_file}")

        # Filter by row indices first (1-based, matching CSV row numbers)
        if row_indices:
            zero_based_indices = [idx - 1 for idx in row_indices if 0 < idx <= len(df)]
            if zero_based_indices:
                df = df.iloc[zero_based_indices].reset_index(drop=True)
                console.print(f"   Filtered to {len(df)} rows by indices: {row_indices}")
            else:
                console.print(f"   [yellow]Warning: No valid row indices found in range 1-{len(df)}[/yellow]")

        if questions:
            column_mapping = _create_column_mapping(df.columns)
            question_col = column_mapping.get("question")
            if question_col:
                df = df[df[question_col].isin(questions)]
                console.print(f"   Filtered to {len(df)} specific questions")

        if limit and limit > 0:
            df = df.head(limit)
            console.print(f"   Limited to first {len(df)} questions")

        return df

    except Exception as e:
        console.print(f"❌ Error loading dataset: {e}")
        raise


def _create_column_mapping(columns: list[str]) -> dict[str, str]:
    """Create case-insensitive column mapping.

    Args:
        columns: List of column names from DataFrame

    Returns:
        Dictionary mapping standard names to actual column names
    """
    column_mapping = {}

    question_keywords = ["question", "questions", "query", "input", "q"]
    answer_keywords = ["answer", "expected_answer", "expected answer", "ground_truth", "a"]
    viz_keywords = ["requires_visualization", "requires visualization", "visualization", "viz"]

    console.print("[cyan]🔍 CSV Column Mapping:[/cyan]")
    console.print(f"   Available columns: {list(columns)}")

    columns_lower = {col.lower(): col for col in columns}

    for keyword in question_keywords:
        if keyword in columns_lower:
            column_mapping["question"] = columns_lower[keyword]
            console.print(f"   ✅ Matched 'question': '{columns_lower[keyword]}'")
            break

    for keyword in answer_keywords:
        if keyword in columns_lower:
            column_mapping["expected_answer"] = columns_lower[keyword]
            console.print(f"   ✅ Matched 'expected_answer': '{columns_lower[keyword]}'")
            break

    for keyword in viz_keywords:
        if keyword in columns_lower:
            column_mapping["requires_visualization"] = columns_lower[keyword]
            console.print(f"   ✅ Matched 'requires_visualization': '{columns_lower[keyword]}'")
            break

    if "question" not in column_mapping:
        raise ValueError(f"Could not find question column. Available columns: {list(columns)}")

    return column_mapping


def get_column_mapping(df: pd.DataFrame) -> dict[str, str]:
    """Get column mapping for a DataFrame.

    Args:
        df: DataFrame to map columns for

    Returns:
        Dictionary mapping standard names to actual column names
    """
    return _create_column_mapping(df.columns)
