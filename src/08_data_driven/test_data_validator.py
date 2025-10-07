"""
Tests demonstrating data-driven testing techniques.
"""
import pytest
import json
import csv
from pathlib import Path
from typing import Dict, Any
from data_validator import DataValidator, User, Product

# Load test data
def load_user_data():
    """Load user test data from CSV."""
    data = []
    csv_path = Path(__file__).parent / "test_data" / "user_data.csv"
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert string values
            row['age'] = int(row['age']) if row['age'] else 0
            row['expected_valid'] = row['expected_valid'].lower() == 'true'
            data.append(row)
    return data

def load_product_data():
    """Load product test data from JSON."""
    json_path = Path(__file__).parent / "test_data" / "product_data.json"
    with open(json_path) as f:
        return json.load(f)

# Test data for parameterization
DATE_TEST_DATA = [
    ("2023-01-01", "%Y-%m-%d", True),
    ("2023/01/01", "%Y/%m/%d", True),
    ("2023-13-01", "%Y-%m-%d", False),
    ("invalid", "%Y-%m-%d", False),
]

PHONE_TEST_DATA = [
    ("+1234567890", True),
    ("12345", False),
    ("+441234567890", True),
    ("invalid", False),
]

CARD_TEST_DATA = [
    ("4532015112830366", True),   # Valid Visa
    ("4532015112830367", False),  # Invalid checksum
    ("12345", False),             # Too short
    ("invalid", False),           # Non-numeric
]

# Fixture for dictionary validation
@pytest.fixture
def sample_dict_schema():
    """Provide sample dictionary validation schema."""
    return {
        "name": str,
        "age": int,
        "active": bool
    }

# Parameterized tests
@pytest.mark.parametrize("date_str,format,expected", DATE_TEST_DATA)
def test_date_validation(date_str, format, expected):
    """Test date validation with different formats."""
    assert DataValidator.validate_date(date_str, format) == expected

@pytest.mark.parametrize("phone,expected", PHONE_TEST_DATA)
def test_phone_validation(phone, expected):
    """Test phone number validation."""
    assert DataValidator.validate_phone(phone) == expected

@pytest.mark.parametrize("card_number,expected", CARD_TEST_DATA)
def test_card_validation(card_number, expected):
    """Test credit card number validation."""
    assert DataValidator.validate_card_number(card_number) == expected

# Data-driven tests using external files
@pytest.mark.parametrize("user_data", load_user_data())
def test_user_validation(user_data):
    """Test user validation with CSV data."""
    user = User(
        name=user_data['name'],
        age=user_data['age'],
        email=user_data['email']
    )
    assert user.is_valid() == user_data['expected_valid']

# Dynamic test generation
def pytest_generate_tests(metafunc):
    """Generate product validation tests dynamically."""
    if "product_data" in metafunc.fixturenames:
        data = load_product_data()
        # Create test cases for both valid and invalid products
        products = [(p, True) for p in data['valid_products']]
        products.extend((p, False) for p in data['invalid_products'])
        metafunc.parametrize("product_data,expected_valid", products)

def test_product_validation(product_data: Dict[str, Any], expected_valid: bool):
    """Test product validation with JSON data."""
    product = Product(**product_data)
    assert product.is_valid() == expected_valid

# Dictionary validation tests
@pytest.mark.parametrize("test_dict,expected", [
    ({"name": "John", "age": 30, "active": True}, True),
    ({"name": "John", "age": "30", "active": True}, False),  # Wrong type
    ({"name": "John", "active": True}, False),  # Missing field
])
def test_dict_validation(test_dict, expected, sample_dict_schema):
    """Test dictionary validation with schema."""
    assert DataValidator.validate_dict(test_dict, sample_dict_schema) == expected