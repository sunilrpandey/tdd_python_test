# Module 8: Data-Driven Testing

This module demonstrates advanced data-driven testing techniques using pytest.

## Features Covered

### 1. Parameterization
- Test function parameterization
- Fixture parameterization
- Parameter IDs and marks
- Custom parameter generation

### 2. Data Sources
- CSV data files
- JSON data files
- YAML configurations
- Database data

### 3. Dynamic Test Generation
- Test matrices
- Generated test cases
- Test combinations
- Dynamic fixtures

### 4. Reusable Test Data
- Shared test data
- Data factories
- Test data builders
- Data validation

## Files in this Module
- `data_validator.py`: Data validation example
- `test_data_validator.py`: Data-driven tests
- `test_data/`: Directory with test data files
- `conftest.py`: Shared fixtures and data
- `README.md`: This file with instructions

## Required Plugins
```bash
pip install pytest-datadir pytest-lazy-fixture
```

## Learning Objectives
1. Master test parameterization
2. Use external data sources
3. Generate dynamic tests
4. Create reusable test data

## Exercise
1. Add new parameterized tests
2. Create data-driven test scenarios
3. Use different data sources
4. Implement data factories