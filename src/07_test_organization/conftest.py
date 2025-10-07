"""
Configuration for pytest including custom markers and plugins.
"""
import pytest
import sys
import platform

def pytest_configure(config):
    """Configure custom markers."""
    # Register custom markers
    config.addinivalue_line("markers", 
        "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers",
        "integration: marks tests as integration tests")
    config.addinivalue_line("markers",
        "requires_network: marks tests that need network access")
    config.addinivalue_line("markers",
        "platform(name): marks tests that run only on named platform")

def pytest_runtest_setup(item):
    """Handle platform-specific markers."""
    for marker in item.iter_markers(name="platform"):
        if marker.args[0] != platform.system():
            pytest.skip(f"Test requires platform {marker.args[0]}")

@pytest.fixture(scope="session")
def network_available():
    """Check if network is available."""
    import socket
    try:
        # Try to connect to a reliable host
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False

def pytest_collection_modifyitems(config, items):
    """Handle requires_network marker."""
    network_marks = []
    for item in items:
        if item.get_closest_marker("requires_network"):
            network_marks.append(item)
    
    if network_marks:
        skip_network = pytest.mark.skip(reason="Test requires network access")
        for item in network_marks:
            item.add_marker(skip_network)