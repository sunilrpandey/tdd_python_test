"""
This module demonstrates different pytest fixture scopes and their behavior.
"""
import pytest

# Counter to track fixture initialization
INIT_COUNTS = {}

def track_init(name):
    """Helper to track how many times a fixture is initialized."""
    INIT_COUNTS[name] = INIT_COUNTS.get(name, 0) + 1
    print(f"\n{name} initialized (count: {INIT_COUNTS[name]})")

# Function Scope (Default)
@pytest.fixture
def function_fixture():
    """
    Function-scoped fixture - created for each test function.
    This is the default scope if none is specified.
    """
    track_init("function_fixture")
    return "function-data"

# Class Scope
@pytest.fixture(scope="class")
def class_fixture():
    """
    Class-scoped fixture - created once per test class.
    Useful for expensive setup needed by all test methods in a class.
    """
    track_init("class_fixture")
    return "class-data"

# Module Scope
@pytest.fixture(scope="module")
def module_fixture():
    """
    Module-scoped fixture - created once per test module.
    Good for resources that can be shared by all tests in the module.
    """
    track_init("module_fixture")
    return "module-data"

# Session Scope
@pytest.fixture(scope="session")
def session_fixture():
    """
    Session-scoped fixture - created once per test session.
    Perfect for very expensive operations needed by many tests.
    """
    track_init("session_fixture")
    return "session-data"

# Test class to demonstrate scope behavior
@pytest.mark.usefixtures("class_fixture")
class TestFixtureScopes:
    """Test class demonstrating fixture scopes."""

    def test_function_scope_1(self, function_fixture):
        """First test using function-scoped fixture."""
        assert function_fixture == "function-data"

    def test_function_scope_2(self, function_fixture):
        """Second test using function-scoped fixture."""
        assert function_fixture == "function-data"

    def test_class_scope_1(self, class_fixture):
        """First test using class-scoped fixture."""
        assert class_fixture == "class-data"

    def test_class_scope_2(self, class_fixture):
        """Second test using class-scoped fixture."""
        assert class_fixture == "class-data"

def test_module_scope_1(module_fixture):
    """First test using module-scoped fixture."""
    assert module_fixture == "module-data"

def test_module_scope_2(module_fixture):
    """Second test using module-scoped fixture."""
    assert module_fixture == "module-data"

def test_session_scope_1(session_fixture):
    """First test using session-scoped fixture."""
    assert session_fixture == "session-data"

def test_session_scope_2(session_fixture):
    """Second test using session-scoped fixture."""
    assert session_fixture == "session-data"