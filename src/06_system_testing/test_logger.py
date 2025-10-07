"""
Tests for Logger demonstrating output capturing and warning testing.
"""
import pytest
import warnings
from logger import Logger, LogLevel

def test_log_output(capsys):
    """Test direct output capture."""
    logger = Logger("TestLogger")
    logger.print_status("Running")
    
    captured = capsys.readouterr()
    assert captured.out == "TestLogger Status: Running\n"
    assert captured.err == ""

def test_log_levels(caplog):
    """Test logging at different levels."""
    logger = Logger("TestLogger")
    
    # Test each log level
    logger.log(LogLevel.DEBUG, "Debug message")
    logger.log(LogLevel.INFO, "Info message")
    logger.log(LogLevel.WARNING, "Warning message")
    logger.log(LogLevel.ERROR, "Error message")
    
    # Verify log records
    assert "Debug message" in caplog.text
    assert "Info message" in caplog.text
    assert "Warning message" in caplog.text
    assert "Error message" in caplog.text

def test_deprecated_method():
    """Test deprecated method warning."""
    logger = Logger("TestLogger")
    
    with pytest.warns(DeprecationWarning, match="This method is deprecated"):
        logger.deprecated_method()
    
    with pytest.warns(DeprecationWarning, match="Custom message"):
        logger.deprecated_method("Custom message")

def test_process_with_warning():
    """Test different types of warnings."""
    logger = Logger("TestLogger")
    
    # Test FutureWarning for negative values
    with pytest.warns(FutureWarning, match="Negative values are deprecated"):
        result = logger.process_with_warning(-5)
        assert result == 5
    
    # Test PendingDeprecationWarning for zero
    with pytest.warns(PendingDeprecationWarning):
        result = logger.process_with_warning(0)
        assert result == 0
    
    # No warning for positive values
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # Turn warnings into errors
        result = logger.process_with_warning(10)
        assert result == 10

def test_warning_filter():
    """Test warning filters."""
    logger = Logger("TestLogger")
    
    # Filter out the deprecation warning
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    logger.deprecated_method()  # Should not raise warning
    
    # Reset warning filters
    warnings.resetwarnings()
    
    # Verify warnings are back
    with pytest.warns(DeprecationWarning):
        logger.deprecated_method()