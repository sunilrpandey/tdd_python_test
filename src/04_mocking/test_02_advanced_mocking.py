"""
Tests demonstrating advanced mocking concepts.
"""
import pytest
from unittest.mock import Mock, patch, create_autospec
from database_client import DatabaseClient

# region Spy Objects
def test_spy_object():
    """
    Demonstrates using a spy object (a mock wrapping a real object).
    Learning points:
    1. Creating a spy
    2. Tracking calls while maintaining real behavior
    3. Verifying interactions with the real object
    """
    # Create a real object
    real_db = DatabaseClient()
    
    # Create a spy that wraps the real object
    spy_db = Mock(wraps=real_db)
    
    # Use the spy - the real method runs, but calls are tracked
    spy_db.get_config()
    
    # Verify the method was called
    assert spy_db.get_config.called
    
    # The real method was actually executed
    assert isinstance(spy_db.get_config(), dict)

# endregion

# region Patch Decorators
@patch('time.sleep')  # Mock sleep to speed up tests
def test_patch_decorator_basic(mock_sleep):
    """
    Shows how to use patch decorator to mock external dependencies.
    Learning points:
    1. Using @patch decorator
    2. Mocking external libraries
    3. Verifying calls to external dependencies
    """
    db = DatabaseClient()
    db.connect()  # This would normally sleep
    
    # Verify sleep was called
    mock_sleep.assert_called_with(1)
    
    # The operation completed without actual delays
    assert db.connected is True

@patch('logging.getLogger')
@patch('time.sleep')
def test_multiple_patches(mock_sleep, mock_get_logger):
    """
    Shows how to patch multiple dependencies.
    Learning points:
    1. Using multiple patch decorators
    2. Understanding decorator order
    3. Mocking multiple dependencies
    """
    # Create a mock logger
    mock_logger = Mock()
    mock_get_logger.return_value = mock_logger
    
    # Use the database client
    db = DatabaseClient()
    db.connect()
    
    # Verify logging occurred
    mock_logger.info.assert_called_with(
        "Connecting to database at localhost:5432"
    )
    
    # Verify sleep was called
    mock_sleep.assert_called_with(1)

# endregion

# region Auto-spec Mocks
def test_autospec_mock():
    """
    Shows how to create strict mocks that enforce the real object's interface.
    Learning points:
    1. Creating auto-spec mocks
    2. Understanding interface enforcement
    3. Catching interface violations
    """
    # Create an auto-spec mock
    mock_db = create_autospec(DatabaseClient)
    
    # This works because execute_query is a real method
    mock_db.execute_query.return_value = {"id": "1"}
    result = mock_db.execute_query("SELECT * FROM users")
    assert result == {"id": "1"}
    
    # This raises AttributeError because fake_method doesn't exist
    with pytest.raises(AttributeError):
        mock_db.fake_method()
    
    # This raises TypeError because execute_query requires an argument
    with pytest.raises(TypeError):
        mock_db.execute_query()

# endregion

# region Complex Mocking Scenarios
def test_conditional_behavior():
    """
    Shows how to create mocks with conditional behavior.
    Learning points:
    1. Using side_effect with functions
    2. Creating dynamic mock behavior
    3. Simulating complex scenarios
    """
    mock_db = Mock()
    
    # Mock conditional behavior
    def query_handler(query):
        if "SELECT" in query:
            return {"id": "1", "name": "test"}
        elif "INSERT" in query:
            return {"status": "inserted"}
        else:
            raise ValueError("Invalid query")
    
    mock_db.execute_query.side_effect = query_handler
    
    # Test different queries
    assert mock_db.execute_query("SELECT * FROM users") == {"id": "1", "name": "test"}
    assert mock_db.execute_query("INSERT INTO users") == {"status": "inserted"}
    with pytest.raises(ValueError):
        mock_db.execute_query("INVALID QUERY")

def test_stateful_mock():
    """
    Shows how to create mocks that maintain state.
    Learning points:
    1. Creating stateful mocks
    2. Simulating real object behavior
    3. Testing state-dependent operations
    """
    mock_db = Mock()
    mock_db.connected = False
    
    # Simulate connect/disconnect behavior
    def connect():
        mock_db.connected = True
        return True
    
    def disconnect():
        mock_db.connected = False
    
    mock_db.connect.side_effect = connect
    mock_db.disconnect.side_effect = disconnect
    
    # Test state changes
    assert mock_db.connected is False
    mock_db.connect()
    assert mock_db.connected is True
    mock_db.disconnect()
    assert mock_db.connected is False

# endregion