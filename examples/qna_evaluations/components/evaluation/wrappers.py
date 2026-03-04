"""Evaluator wrappers for debugging and logging.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

"""

import logging
import time


class LoggingEvaluatorWrapper:
    """Wrapper to log evaluator execution WITHOUT interfering with retry mechanism.
    
    This wrapper adds detailed logging for debugging evaluation failures and timing issues.
    It does NOT interfere with the underlying evaluator's retry mechanism.
    """
    
    def __init__(self, evaluator, name: str):
        """Initialize the logging wrapper.
        
        Args:
            evaluator: The evaluator instance to wrap
            name: Name for logging purposes
        """
        self.evaluator = evaluator
        self.name = name
        self.metrics = evaluator.metrics
        self._setup_logger()
        
    def _setup_logger(self):
        """Setup file logger for this evaluator."""
        self.logger = logging.getLogger(f'evaluator_{self.name}')
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler if not exists
        if not self.logger.handlers:
            fh = logging.FileHandler(f'evaluator_{self.name}_debug.log', mode='w')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(fh)
        
    async def evaluate(self, data):
        """Wrapped evaluate with logging - NO timeout to allow retries.
        
        Args:
            data: Data to evaluate
            
        Returns:
            Evaluation result from wrapped evaluator
            
        Raises:
            Exception: Any exception from the wrapped evaluator
        """
        start_time = time.time()
        
        self.logger.info(f"=== Starting {self.name} evaluation ===")
        self.logger.info(f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'not a dict'}")
        self.logger.info(f"Number of metrics: {len(self.metrics)}")
        
        try:
            self.logger.info("Calling evaluator.evaluate() - allowing native retry mechanism...")
            # NO asyncio.wait_for() - let the evaluator's retry mechanism work!
            result = await self.evaluator.evaluate(data)
            
            elapsed = time.time() - start_time
            self.logger.info(f"✅ Evaluation completed successfully in {elapsed:.2f}s!")
            self.logger.info(f"Result type: {type(result)}")
            self.logger.info(f"Result: {result}")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"❌ EXCEPTION after {elapsed:.2f}s: {type(e).__name__}")
            self.logger.error(f"Error message: {str(e)}")
            import traceback
            self.logger.error(f"Traceback:\n{traceback.format_exc()}")
            raise
