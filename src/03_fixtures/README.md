# Understanding Pytest Fixtures

This module demonstrates the various features and capabilities of pytest fixtures through practical examples.

## Key Concepts Covered

### 1. Basic Fixture Concepts (`test_database.py`)
- Basic fixture usage for setup and teardown
- Database connection simulation
- Test data management
- Simple fixture patterns

### 2. Fixture Scopes (`test_fixture_scopes.py`)
Different fixture scopes and their use cases:
- **Function scope** (default): Created for each test function
- **Class scope**: Created once per test class
- **Module scope**: Created once per test module
- **Session scope**: Created once per test session

### 3. Fixture Dependencies (`test_fixture_dependencies.py`)
- How fixtures can depend on other fixtures
- Building complex test scenarios
- Sharing fixtures across tests
- Combining multiple fixtures

### 4. Parameterized Fixtures (`test_parameterized_fixtures.py`)
- Basic parameter usage
- Custom parameter IDs
- Complex data structures as parameters
- Combining with `pytest.mark.parametrize`

## Running the Examples

### Basic Usage
```bash
# Run all fixture examples
pytest

# Run with verbose output to see fixture initialization
pytest -v

# Show fixture initialization order
pytest --setup-show
```

### Running Specific Examples
```bash
# Run basic database tests
pytest test_database.py

# Run fixture scope examples
pytest test_fixture_scopes.py -v

# Run dependency examples
pytest test_fixture_dependencies.py

# Run parameterized fixture examples
pytest test_parameterized_fixtures.py
```

## Key Points to Remember

1. **Fixture Scopes**
   - Function: Fresh fixture for each test function
   - Class: Shared across all methods in a test class
   - Module: Shared across all tests in a module
   - Session: Shared across all tests in the test session

2. **Fixture Dependencies**
   - Fixtures can use other fixtures
   - Dependencies are resolved automatically
   - Can create complex test scenarios

3. **Parameterization**
   - Run same test with different inputs
   - Custom IDs for better test naming
   - Can combine with regular fixtures

4. **Best Practices**
   - Keep fixtures focused and simple
   - Use appropriate scope to optimize performance
   - Document fixture purpose and dependencies
   - Use meaningful names for fixtures

## Examples in Detail

### Basic Database Testing
```python
@pytest.fixture
def db():
    """Create a new database instance for each test."""
    database = Database()
    yield database
    database.clear()
```

### Fixture Scopes
```python
@pytest.fixture(scope="session")
def session_fixture():
    """Created once for the entire test session."""
    return "session-data"
```

### Fixture Dependencies
```python
@pytest.fixture
def populated_db(db, sample_data):
    """Combine database and data fixtures."""
    for record in sample_data:
        db.insert("users", record)
    return db
```

### Parameterized Fixtures
```python
@pytest.fixture(params=["users", "products", "orders"])
def table_name(request):
    """Provide different table names for tests."""
    return request.param
```

## Debugging Tests

### Using the -k Option
The `-k` option in pytest allows you to selectively run tests based on their names. This is extremely useful for debugging specific test failures or focusing on particular test cases.

```bash
# Run tests with specific name pattern
pytest -k "test_specific_datasets"  # Runs only tests containing "test_specific_datasets" in their name

# Using logical operators
pytest -k "test and not simple"     # Runs tests with "test" but not "simple" in their name
pytest -k "dataset or simple"       # Runs tests with either "dataset" or "simple" in their name
pytest -k "not test_simple"         # Runs all tests except those with "test_simple" in their name
```

Common debugging patterns:
- Use `-k` with specific test names when investigating failures
- Combine with `-v` for verbose output: `pytest -v -k "test_name"`
- Use with test class names: `pytest -k TestClassName`
- Combine multiple conditions: `pytest -k "TestClass and not test_skip"`

## Additional Resources

- [Pytest Documentation on Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Pytest Documentation on Parametrization](https://docs.pytest.org/en/stable/parametrize.html)
- [Pytest Documentation on Test Selection](https://docs.pytest.org/en/stable/usage.html#specifying-tests-selecting-tests)