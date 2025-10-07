"""
Data processor class to demonstrate advanced pytest features.
"""
from typing import List, Any, Optional
from enum import Enum, auto

class ProcessingMode(Enum):
    """Processing modes for data transformation."""
    STRICT = auto()
    LENIENT = auto()

class DataProcessor:
    """A class for processing and validating data."""
    
    def __init__(self, mode: ProcessingMode = ProcessingMode.STRICT):
        """Initialize the data processor."""
        self.mode = mode
    
    def process_numbers(self, numbers: List[Any]) -> List[float]:
        """Process a list of numbers, converting strings to floats."""
        result = []
        
        for num in numbers:
            try:
                if isinstance(num, str):
                    # Remove whitespace and handle percentage
                    cleaned = num.strip().rstrip('%')
                    value = float(cleaned)
                    if num.endswith('%'):
                        value /= 100
                else:
                    value = float(num)
                result.append(value)
            except (ValueError, TypeError):
                if self.mode == ProcessingMode.STRICT:
                    raise ValueError(f"Invalid number: {num}")
                # In lenient mode, skip invalid values
        
        return result
    
    def calculate_statistics(self, numbers: List[Any]) -> Optional[dict]:
        """Calculate basic statistics for a list of numbers."""
        try:
            processed = self.process_numbers(numbers)
            if not processed:
                return None
            
            return {
                "count": len(processed),
                "sum": sum(processed),
                "average": sum(processed) / len(processed),
                "min": min(processed),
                "max": max(processed)
            }
        except ValueError:
            if self.mode == ProcessingMode.STRICT:
                raise
            return None