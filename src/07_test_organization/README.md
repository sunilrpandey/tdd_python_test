# Module 7: Test Organization and Execution

This module demonstrates advanced test organization features and execution strategies in pytest.

## Features Covered

### 1. Custom Markers
- Creating custom markers
- Marker expressions
- Marker inheritance
- Marker documentation

### 2. Test Categories
- Integration tests
- Slow tests
- Platform-specific tests
- Configuration-dependent tests

### 3. Parallel Test Execution
- Using pytest-xdist
- Test isolation
- Resource management
- Performance optimization

### 4. Test Retries
- Flaky test handling
- Retry conditions
- Maximum retry limits
- Retry reporting

## Files in this Module
- `order_processor.py`: Example business logic
- `test_order_processor.py`: Tests with different categories
- `conftest.py`: Custom markers and configurations
- `pytest.ini`: Pytest configuration
- `README.md`: This file with instructions

## Required Plugins
```bash
pip install pytest-xdist pytest-rerunfailures
```

## Running Tests
```bash
# Run tests in parallel
pytest -n auto

# Run only slow tests
pytest -m slow

# Run with retries for flaky tests
pytest --reruns 3

# Run specific test categories
pytest -m "integration and not slow"
```

## Learning Objectives
1. Organize tests with markers
2. Execute tests in parallel
3. Handle flaky tests
4. Manage test categories

## Exercise
1. Add new custom markers
2. Create parallel-safe tests
3. Configure test retries
4. Organize tests by category