# Module 3: pytest Fixtures

This module demonstrates the power and flexibility of pytest fixtures.

## What are Fixtures?
Fixtures are functions that provide test data or test resources to test functions. They help in:
- Setting up test data
- Creating reusable test resources
- Managing test state
- Cleaning up after tests

## Key Concepts

### 1. Fixture Scopes
- `function`: Run once per test function (default)
- `class`: Run once per test class
- `module`: Run once per module
- `session`: Run once per test session

### 2. Fixture Features
- Dependency injection
- Automatic cleanup with yield fixtures
- Factory fixtures
- Parameterization

## Files in this Module
- `database.py`: A simple database simulator
- `test_database.py`: Tests demonstrating fixture usage
- `conftest.py`: Shared fixtures
- `README.md`: This file with instructions

## Learning Objectives
1. Understand fixture basics
2. Learn about fixture scopes
3. Practice fixture parameterization
4. Understand fixture dependencies

## Exercise
1. Run the provided tests
2. Add new fixtures with different scopes
3. Create parameterized fixtures
4. Implement fixtures with cleanup using yield