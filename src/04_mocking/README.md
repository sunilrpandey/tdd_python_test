# Understanding Mocking in Python Tests

This module provides a comprehensive guide to mocking in Python tests, using a simple database example to demonstrate various mocking techniques and concepts.

## Learning Objectives
1. Understand mocking basics and their purpose in testing
2. Learn about different types of mocks and when to use each
3. Practice mocking external dependencies effectively
4. Master mock assertions and verifications

## Debugging Mock Tests

### 1. Using -v for Verbose Output
```bash
# Run with verbose output to see test names and results
pytest -v test_01_basic_mocking.py
```

### 2. Using -k for Specific Tests
```bash
# Run specific test by name
pytest -v -k "test_mock_basic_return_value"

# Run tests matching a pattern
pytest -v -k "basic"
```

### 3. Using pdb for Interactive Debugging
```bash
# Add breakpoint in your test:
import pdb; pdb.set_trace()

# Or run pytest with --pdb flag to break on failure
pytest --pdb

# Common pdb commands:
# n - next line
# s - step into
# c - continue
# p variable - print variable
# l - show current location
```

### 4. Using print() with -s Flag
```bash
# Allow print statements to show in output
pytest -v -s

# In your test:
def test_something():
    mock_db = Mock()
    print(f"Mock calls: {mock_db.method_calls}")
```

### 5. Inspecting Mock Objects
```python
# Print all recorded calls
print(mock_db.method_calls)

# Print call arguments
print(mock_db.execute_query.call_args)

# Print call count
print(mock_db.execute_query.call_count)
```

### 6. Using --setup-show
```bash
# Show test setup and teardown
pytest --setup-show

# Helps understand fixture and mock initialization
```

### 7. Using -x for Early Exit
```bash
# Stop after first failure
pytest -x

# Useful when debugging specific failures
```

### 8. Mock Debugging Tips
1. Check if your mock is being used:
   ```python
   assert mock_db.execute_query.called
   ```

2. Verify mock configuration:
   ```python
   print(f"Return value: {mock_db.execute_query.return_value}")
   print(f"Side effect: {mock_db.execute_query.side_effect}")
   ```

3. Inspect call history:
   ```python
   for call in mock_db.method_calls:
       print(f"Method: {call[0]}, Args: {call[1]}, Kwargs: {call[2]}")
   ```

## Key Concepts

### What is Mocking?
Mocking is a technique used in unit testing to replace real objects with test doubles that simulate their behavior. This is particularly useful when testing:
- Code with external dependencies (databases, networks, etc.)
- Code with time-dependent operations (like our database delays)
- Code with complex setup requirements
- Code with non-deterministic behavior

### Types of Mocks

#### 1. Mock Objects (`Mock` and `MagicMock`)
Basic test doubles that can simulate any object:
```python
# Create a basic mock
mock_connection = Mock()
mock_connection.connected = True
mock_connection.get.return_value = {"id": "1", "name": "Alice"}
```

#### 2. Spy Objects
Mocks that can track calls while optionally maintaining real behavior:
```python
# Create a spy from a real object
real_connection = DatabaseConnection()
spy_connection = Mock(wraps=real_connection)
```

#### 3. Patch Decorators
Tools for replacing objects in the scope of a test:
```python
@patch('time.sleep')
def test_function(mock_sleep):
    # time.sleep is now mocked in database operations
    pass
```

#### 4. Auto-spec Mocks
Strict mocks that enforce the real object's interface:
```python
# Create a mock that only allows real methods
mock_connection = Mock(spec=DatabaseConnection)
```

### Mock Features

#### 1. Return Values
Configure what values mocked methods should return:
```python
mock_connection.get.return_value = {"id": "1", "name": "Alice"}
```

#### 2. Side Effects
Add dynamic behavior to mocked methods:
```python
# Simulate database errors
def db_error(*args):
    raise RuntimeError("Database error")
mock_connection.insert.side_effect = db_error
```

#### 3. Call Tracking
Monitor how mocks are used:
```python
db.insert("users", {"id": "1", "name": "Alice"})
mock_connection.insert.assert_called_once()
```

#### 4. Assertions on Calls
Verify how mocks were used in tests:
```python
mock_connection.assert_has_calls([
    call.connect(),
    call.insert("users", {"id": "1", "name": "Alice"}),
    call.disconnect()
])
```

## Files in this Module
- `database.py`: A simple database simulator with external dependencies
- `test_database_mocking.py`: Comprehensive mocking examples
- `README.md`: This documentation

## Examples in Practice

### Basic Mocking
```python
def test_basic_mock():
    # Create a mock database connection
    mock_connection = Mock()
    mock_connection.connected = True
    
    # Use the mock in our database
    db = Database(mock_connection)
    result = db.insert("users", {"id": "1", "name": "Alice"})
    
    assert result is True
```

### Mocking Time Delays
```python
@patch('time.sleep')
def test_performance(mock_sleep):
    conn = DatabaseConnection()
    conn.connect()  # Won't actually sleep
    mock_sleep.assert_called_once_with(1)
```

## Running the Tests

```bash
# Run all mocking tests
pytest test_database_mocking.py

# Run specific test categories
pytest test_database_mocking.py -k "mock_side_effects"
pytest test_database_mocking.py -k "patch"

# Run with verbose output
pytest -v test_database_mocking.py
```

## Best Practices

1. **Mock at the Right Level**
   - Mock external dependencies (like time.sleep)
   - Don't mock the class you're testing
   - Mock at the boundaries of your system

2. **Keep Mocks Simple**
   - Only mock what you need
   - Use the simplest mock type that works
   - Don't mock what you don't own

3. **Use Meaningful Names**
   - Name mocks after what they replace
   - Use descriptive test names
   - Document complex mock setups

4. **Verify Behavior, Not Implementation**
   - Test what the code does
   - Focus on external behavior
   - Don't over-specify mock expectations

## Exercise
1. Run the provided tests
2. Add new test cases with different mock scenarios
3. Try different mock configurations
4. Implement error case testing with mocks

## Additional Resources

- [Python unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-mock Plugin Documentation](https://pytest-mock.readthedocs.io/)
- [Real Python Mocking Tutorial](https://realpython.com/python-mock-library/)