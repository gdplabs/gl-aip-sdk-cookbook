"""Components package for GLAIP Agent Benchmark System.

This package contains modular components for agent benchmarking and evaluation.
Refactored into logical submodules: evaluation/, data/, and capture/.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

__version__ = "2.1.0"
__author__ = "Daniel Adi (daniel.adi@gdplabs.id)"

# Core config
from .config import BenchmarkConfig

# Evaluation components
from .evaluation import ComprehensiveAgentEvaluator, LoggingEvaluatorWrapper, ArtifactValidationMetric

# Data handling components
from .data import (
    build_result_row_from_inference,
    convert_experiment_tracker_results,
    get_column_mapping,
    load_dataset,
    save_results,
)

# Capture components
from .capture import AsyncEventProcessor, OptimizedCLIAgentRenderer

# Utilities
from .utils import reorder_columns_with_parts, thread_safe_print

# Backward compatibility: CSVHandler class wrapper
class CSVHandler:
    """Backward compatibility wrapper for old CSVHandler interface.
    
    This class maintains the old static method interface while delegating
    to the new modular structure.
    """
    
    @staticmethod
    def load_dataset(*args, **kwargs):
        return load_dataset(*args, **kwargs)
    
    @staticmethod
    def get_column_mapping(*args, **kwargs):
        return get_column_mapping(*args, **kwargs)
    
    @staticmethod
    def save_results(*args, **kwargs):
        return save_results(*args, **kwargs)
    
    @staticmethod
    def convert_experiment_tracker_results(*args, **kwargs):
        return convert_experiment_tracker_results(*args, **kwargs)
    
    @staticmethod
    def build_result_row_from_inference(*args, **kwargs):
        return build_result_row_from_inference(*args, **kwargs)


__all__ = [
    # Config
    "BenchmarkConfig",
    # Evaluation
    "ArtifactValidationMetric",
    "ComprehensiveAgentEvaluator",
    "LoggingEvaluatorWrapper",
    # Data
    "CSVHandler",  # Backward compatibility
    "load_dataset",
    "get_column_mapping",
    "save_results",
    "convert_experiment_tracker_results",
    "build_result_row_from_inference",
    # Capture
    "AsyncEventProcessor",
    "OptimizedCLIAgentRenderer",
    # Utils
    "reorder_columns_with_parts",
    "thread_safe_print",
]
