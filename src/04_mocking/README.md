# Module 4: Mocking in pytest

This module demonstrates how to use mocking in pytest using both `unittest.mock` and `pytest-mock`.

## What is Mocking?
Mocking is a technique used in testing to replace real objects with mock objects that simulate their behavior. It's useful for:
- Isolating the code being tested
- Testing code that depends on external services
- Simulating different scenarios and edge cases
- Testing error conditions

## Key Concepts

### 1. Types of Mocks
- Mock objects
- Spy objects
- Patch decorators
- Auto-spec mocks

### 2. Mock Features
- Return values
- Side effects
- Call tracking
- Assertions on calls

## Files in this Module
- `weather_service.py`: A weather service client
- `test_weather_service.py`: Tests demonstrating mocking
- `README.md`: This file with instructions

## Learning Objectives
1. Understand mocking basics
2. Learn about different types of mocks
3. Practice mocking external dependencies
4. Master mock assertions and verifications

## Exercise
1. Run the provided tests
2. Add new test cases with different mock scenarios
3. Try different mock configurations
4. Implement error case testing with mocks