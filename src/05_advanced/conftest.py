"""
Configuration and shared fixtures for advanced pytest features.
"""
import pytest
from data_processor import ProcessingMode

def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "data_processing: marks tests related to data processing"
    )

@pytest.fixture(params=[ProcessingMode.STRICT, ProcessingMode.LENIENT])
def processor_mode(request):
    """Parameterized fixture providing processing modes."""
    return request.param

@pytest.fixture
def sample_datasets():
    """Provide sample datasets for testing."""
    return [
        [1, 2, 3, 4, 5],
        ["1", "2", "3", "4", "5"],
        ["10%", "20%", "30%", "40%", "50%"],
        [],
        ["invalid", 1, 2, 3],
    ]