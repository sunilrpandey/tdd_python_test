"""
Logger utility demonstrating output capturing and warnings.
"""
import logging
import warnings
from typing import Optional
from enum import Enum, auto

class LogLevel(Enum):
    """Log levels for the logger."""
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()

class Logger:
    """Custom logger with output and warning demonstrations."""
    
    def __init__(self, name: str):
        """Initialize logger with name."""
        self.name = name
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Set up the logger configuration."""
        self.logger = logging.getLogger(self.name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)
    
    def log(self, level: LogLevel, message: str) -> None:
        """Log a message at the specified level."""
        if level == LogLevel.DEBUG:
            self.logger.debug(message)
        elif level == LogLevel.INFO:
            self.logger.info(message)
        elif level == LogLevel.WARNING:
            self.logger.warning(message)
        elif level == LogLevel.ERROR:
            self.logger.error(message)
    
    @staticmethod
    def deprecated_method(message: Optional[str] = None) -> None:
        """Example of a deprecated method that raises a warning."""
        warnings.warn(
            message or "This method is deprecated",
            DeprecationWarning,
            stacklevel=2
        )
    
    def print_status(self, status: str) -> None:
        """Print status directly to stdout."""
        print(f"{self.name} Status: {status}")
    
    def process_with_warning(self, value: int) -> int:
        """Process a value with potential warning."""
        if value < 0:
            warnings.warn("Negative values are deprecated", FutureWarning)
        elif value == 0:
            warnings.warn("Zero values may be unsupported in future", PendingDeprecationWarning)
        return abs(value)