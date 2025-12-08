"""
Examples of debugging techniques for mock tests.
Add this to test_01_basic_mocking.py
"""
from unittest.mock import Mock

def test_debugging_example():
    """
    This test demonstrates various debugging techniques.
    Run with: pytest -v -s test_01_basic_mocking.py -k test_debugging_example
    """
    # Create a mock
    mock_db = Mock()
    mock_db.connected = True
    mock_db.execute_query.return_value = {"id": "1", "name": "test"}
    
    # Example 1: Print mock state
    print("\nMock initial state:")
    print(f"Connected: {mock_db.connected}")
    print(f"Return value: {mock_db.execute_query.return_value}")
    
    # Make some calls
    mock_db.execute_query("SELECT * FROM users")
    mock_db.execute_query("INSERT INTO users VALUES id=1")
    
    # Example 2: Inspect calls
    print("\nCall information:")
    print(f"Call count: {mock_db.execute_query.call_count}")
    print(f"Call arguments: {mock_db.execute_query.call_args_list}")
    
    # Example 3: Detailed call inspection
    print("\nDetailed call history:")
    for i, call in enumerate(mock_db.execute_query.call_args_list, 1):
        args = call[0]  # positional arguments
        kwargs = call[1]  # keyword arguments
        print(f"\nCall {i}:")
        print(f"  Args: {args}")
        print(f"  Kwargs: {kwargs}")
    
    # Example 4: Method call history
    print("\nAll method calls:")
    print(mock_db.method_calls)
    
    # Example 5: Using pdb (uncomment to use)
    # import pdb; pdb.set_trace()
    
    # Assertions for the test
    assert mock_db.execute_query.call_count == 2
    assert "SELECT" in mock_db.execute_query.call_args_list[0][0][0]
    assert "INSERT" in mock_db.execute_query.call_args_list[1][0][0]

def test_side_effect_debugging():
    """
    Demonstrates debugging side effects and dynamic behaviors.
    Run with: pytest -v -s test_01_basic_mocking.py -k test_side_effect_debugging
    """
    mock_db = Mock()
    
    # Set up a side effect function with print statements
    def side_effect(query):
        print(f"\nExecuting query: {query}")
        if "SELECT" in query:
            print("Returning select result")
            return {"id": "1", "name": "test"}
        elif "INSERT" in query:
            print("Returning insert result")
            return {"status": "inserted"}
        else:
            print("Raising error")
            raise ValueError("Invalid query")
    
    mock_db.execute_query.side_effect = side_effect
    
    # Try different queries
    print("\nTesting SELECT:")
    result1 = mock_db.execute_query("SELECT * FROM users")
    print(f"Result: {result1}")
    
    print("\nTesting INSERT:")
    result2 = mock_db.execute_query("INSERT INTO users VALUES id=1")
    print(f"Result: {result2}")
    
    print("\nTesting invalid query:")
    try:
        mock_db.execute_query("INVALID QUERY")
    except ValueError as e:
        print(f"Caught error: {e}")
    
    # Assertions
    assert mock_db.execute_query.call_count == 3