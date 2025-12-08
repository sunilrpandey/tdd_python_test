"""
Tests demonstrating basic mocking concepts.
"""
import pytest
from unittest.mock import Mock
from database_client import DatabaseClient

def test_mock_basic_return_value():
    """
    Basic example: Mocking an object's attribute and method return value.
    Learning points:
    1. Creating a basic mock object
    2. Setting mock attributes
    3. Setting return values for mock methods
    """
    # Create a mock object
    mock_db = Mock()
    
    
    # Set up the mock
    mock_db.connected = True  # Mock an attribute
    mock_db.execute_query.return_value = {"id": "1", "name": "test"}  # Mock a method return value
    
    # Use the mock
    assert mock_db.connected is True
    result = mock_db.execute_query("SELECT * FROM users")
    assert result == {"id": "1", "name": "test"}

def test_mock_with_real_object():
    """
    Shows how to partially mock a real object.
    Learning points:
    1. Working with real objects
    2. Mocking specific methods while keeping others real
    """
    # Create a real database client
    db = DatabaseClient()
    
    # Replace specific method with a mock
    original_execute_query = db.execute_query
    db.execute_query = Mock(return_value={"id": "1", "name": "test"})
    
    try:
        # Use the mocked method
        result = db.execute_query("SELECT * FROM users")
        assert result == {"id": "1", "name": "test"}
        
        # Other methods still work normally
        assert isinstance(db.get_config(), dict)
    finally:
        # Restore original method
        db.execute_query = original_execute_query

def test_mock_multiple_return_values():
    """
    Shows how to mock multiple return values.
    Learning points:
    1. Setting up sequence of return values
    2. Mock remembers calls and returns values in order
    """
    # Create mock with multiple return values
    mock_db = Mock()
    mock_db.execute_query.side_effect = [
        {"id": "1", "name": "first"},
        {"id": "2", "name": "second"},
        None  # Simulate a failed query
    ]
    
    # First call
    assert mock_db.execute_query("SELECT * FROM users") == {"id": "1", "name": "first"}
    
    # Second call
    assert mock_db.execute_query("SELECT * FROM users") == {"id": "2", "name": "second"}
    
    # Third call
    assert mock_db.execute_query("SELECT * FROM users") is None

def test_mock_raising_exception():
    """
    Shows how to mock methods that raise exceptions.
    Learning points:
    1. Making mocks raise exceptions
    2. Testing error handling
    """
    # Create mock that raises an exception
    mock_db = Mock()
    mock_db.execute_query.side_effect = ValueError("Invalid query")
    
    # Verify that the exception is raised
    with pytest.raises(ValueError) as exc_info:
        mock_db.execute_query("INVALID QUERY")
    assert str(exc_info.value) == "Invalid query"

def test_mock_call_tracking():
    """
    Shows how to track mock calls.
    Learning points:
    1. Verifying if methods were called
    2. Checking call arguments
    3. Verifying call count
    """
    # Create mock
    mock_db = Mock()
    
    # Call the mock several times
    mock_db.execute_query("SELECT * FROM users")
    mock_db.execute_query("INSERT INTO users VALUES id=1")
    
    # Verify calls
    assert mock_db.execute_query.call_count == 2
    
    # Check last call arguments
    last_call_args = mock_db.execute_query.call_args[0][0]
    assert "INSERT INTO users" in last_call_args
    
    # Verify all calls
    all_calls = mock_db.execute_query.call_args_list
    assert "SELECT * FROM users" in all_calls[0][0][0]