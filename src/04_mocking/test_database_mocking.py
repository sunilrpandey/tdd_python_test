"""
Test module demonstrating different types of mocks and their features.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
from database import Database, DatabaseConnection

# region Mock Connection State Examples

def test_database_connection_state():
    """
    Demonstrates mocking just the connection state.
    The actual database operations will use real implementation.
    """
    # Create a mock connection with connected state
    mock_connection = Mock()
    mock_connection.connected = True
    
    # Create database with mock connection
    db = Database(mock_connection)
    
    # Insert will work because connection.connected is True
    result = db.insert("users", {"id": "1", "name": "Alice"})
    assert result is True
    
    # Verify the data was actually stored in db._data
    stored_data = db._data["users"]["1"]
    assert stored_data["name"] == "Alice"
    
    # Now simulate disconnected state
    mock_connection.connected = False
    
    # Insert should fail when not connected
    result = db.insert("users", {"id": "2", "name": "Bob"})
    assert result is False

def test_mock_return_values():
    """
    Shows how to test database operations with a mocked connection.
    Demonstrates that Database methods use real implementation while only connection state is mocked.
    """
    mock_connection = Mock()
    mock_connection.connected = True
    
    # Create database with mock connection
    db = Database(mock_connection)
    
    # Insert some test data (using real Database implementation)
    db.insert("users", {"id": "1", "name": "Alice"})
    
    # Test get operation - this uses the real implementation, not a mock
    retrieved_data = db.get("users", "1")
    assert retrieved_data["name"] == "Alice"
    
    # Test update operation - this uses the real implementation, not a mock
    db.update("users", "1", {"name": "Bob"})
    updated_data = db.get("users", "1")
    assert updated_data["name"] == "Bob"
    
    # Only the connection state was mocked
    assert mock_connection.connected is True

# endregion

# region Spy Objects

def test_spy_object():
    """
    Demonstrates using a mock as a spy to track calls.
    Shows how to verify what calls were made to the mock.
    """
    # Create a spy
    mock_connection = Mock()
    mock_connection.connected = True
    
    # Use the spy
    db = Database(mock_connection)
    db.insert("users", {"id": "1", "name": "Alice"})
    db.insert("users", {"id": "2", "name": "Bob"})
    
    # Check call counts
    assert mock_connection.method_calls  # Verify methods were called
    
    # You can also create a spy from a real object
    real_connection = DatabaseConnection()
    spy_connection = Mock(wraps=real_connection)
    db = Database(spy_connection)
    
    # Now you can track calls while using the real object
    db.insert("users", {"id": "3", "name": "Charlie"})
    assert spy_connection.method_calls

# endregion

# region Patch Decorator Examples

@patch('time.sleep')  # Mock the sleep function
def test_patch_decorator(mock_sleep):
    """
    Shows how to use the @patch decorator to mock functions.
    Demonstrates mocking external dependencies.
    """
    # Create a real connection (sleep will be mocked)
    conn = DatabaseConnection()
    conn.connect()  # This won't actually sleep
    
    # Verify sleep was called
    mock_sleep.assert_called_once_with(1)
    
    # The connection should work as normal
    assert conn.connected is True

@patch('logging.getLogger')
@patch('time.sleep')
def test_multiple_patches(mock_sleep, mock_get_logger):
    """
    Demonstrates using multiple patch decorators.
    Shows how to mock multiple dependencies.
    """
    mock_logger = Mock()
    mock_get_logger.return_value = mock_logger
    
    # Create database objects
    conn = DatabaseConnection()
    db = Database(conn)
    
    # Perform operations
    conn.connect()
    db.insert("users", {"id": "1", "name": "Alice"})
    
    # Verify logging occurred
    assert mock_logger.info.called
    assert mock_logger.debug.called
    
    # Verify no actual sleeping occurred
    assert mock_sleep.called

# endregion

# region Auto-spec Mocks

def test_autospec_mock():
    """
    Shows how to use auto-spec mocks.
    Demonstrates creating strict mocks that enforce the real object's interface.
    """
    # Create an auto-spec mock of DatabaseConnection
    mock_connection = Mock(spec=DatabaseConnection)
    mock_connection.connected = True
    
    db = Database(mock_connection)
    
    # This will work because 'connected' is a real attribute
    assert db.connection.connected is True
    
    # This would raise an AttributeError because 'fake_method' isn't real
    with pytest.raises(AttributeError):
        db.connection.fake_method()

# endregion

# region Side Effects

def test_mock_side_effects():
    """
    Demonstrates using side effects with mocks.
    Shows different ways to make mocks behave dynamically.
    """
    mock_connection = Mock()
    mock_connection.connected = True
    
    # Side effect that counts calls
    call_count = 0
    def side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return call_count
    
    mock_connection.get.side_effect = side_effect
    
    db = Database(mock_connection)
    
    # Each call returns the next number
    assert db.get("users", "1") == 1
    assert db.get("users", "2") == 2
    
    # Side effect that raises an exception
    mock_connection.get.side_effect = RuntimeError("Database error")
    
    # This should return None due to error handling
    assert db.get("users", "3") is None

# endregion

# region Call Assertions

def test_call_assertions():
    """
    Shows different ways to verify how mocks were called.
    Demonstrates various assertion methods available on mocks.
    """
    mock_connection = Mock()
    mock_connection.connected = True
    
    db = Database(mock_connection)
    
    # Perform some operations
    db.insert("users", {"id": "1", "name": "Alice"})
    db.get("users", "1")
    db.update("users", "1", {"name": "Alicia"})
    
    # Assert call counts
    assert mock_connection.method_calls  # Check if any calls were made
    
    # Check specific call order
    expected_calls = [
        call.insert("users", {"id": "1", "name": "Alice"}),
        call.get("users", "1"),
        call.update("users", "1", {"name": "Alicia"})
    ]
    
    # This would verify exact call order
    # mock_connection.assert_has_calls(expected_calls, any_order=False)

# endregion