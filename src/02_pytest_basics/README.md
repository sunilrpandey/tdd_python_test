# Module 2: pytest Basics

This module covers the fundamentals of pytest and its features.

## Key Concepts

### 1. Test Discovery
- Test files must start or end with `test_`
- Test functions must start with `test_`
- Test classes must start with `Test`

### 2. Assertions
- pytest uses Python's built-in `assert` statement
- Provides detailed assertion introspection
- No need to remember assertion method names

### 3. Running Tests
```powershell
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest test_file.py

# Run tests matching a pattern
pytest -k "pattern"
```

## Files in this Module
- `string_utils.py`: A utility class for string operations
- `test_string_utils.py`: Tests demonstrating pytest features
- `README.md`: This file with instructions

## Learning Objectives
1. Understand pytest test discovery
2. Learn about pytest assertions
3. Practice different ways to run tests
4. Understand test organization

## Exercise
1. Run the provided tests
2. Add new test cases using different assertion patterns
3. Try running tests with different pytest options
4. Add new string utility functions using TDD