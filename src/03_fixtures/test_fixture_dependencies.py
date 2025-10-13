"""
This module demonstrates fixture dependencies and sharing in pytest.
"""
import pytest
from database import Database

# Base fixtures that others will depend on
@pytest.fixture
def config():
    """
    Base fixture providing configuration.
    Other fixtures can depend on this to get configuration settings.
    """
    return {
        "db_name": "test_db",
        "tables": ["users", "products", "orders"],
        "admin_user": "admin"
    }

@pytest.fixture
def schema(config):
    """
    Fixture that depends on config fixture.
    Shows how fixtures can use other fixtures' data.
    """
    return {
        table: {
            "name": table,
            "owner": config["admin_user"],
            "created_at": "2025-10-13"
        }
        for table in config["tables"]
    }

@pytest.fixture
def db_with_schema(db, schema):
    """
    Fixture depending on multiple other fixtures.
    Shows how to combine multiple fixtures to create more complex setup.
    """
    # Store schema information in a special table
    for table_name, table_schema in schema.items():
        db.insert("_schemas", {"id": table_name, **table_schema})
    return db

@pytest.fixture
def user_data():
    """Fixture providing user test data."""
    return [
        {"id": "1", "name": "Alice", "role": "admin"},
        {"id": "2", "name": "Bob", "role": "user"}
    ]

@pytest.fixture
def product_data():
    """Fixture providing product test data."""
    return [
        {"id": "1", "name": "Widget", "price": 9.99},
        {"id": "2", "name": "Gadget", "price": 19.99}
    ]

@pytest.fixture
def populated_db_with_all(db_with_schema, user_data, product_data):
    """
    Complex fixture that combines multiple data fixtures.
    Shows how to build complex test scenarios using multiple fixtures.
    """
    # Insert user data
    for user in user_data:
        db_with_schema.insert("users", user)
    
    # Insert product data
    for product in product_data:
        db_with_schema.insert("products", product)
    
    return db_with_schema

def test_schema_creation(db_with_schema, config):
    """Test that schema is correctly created using multiple fixtures."""
    for table in config["tables"]:
        schema_info = db_with_schema.get("_schemas", table)
        assert schema_info["owner"] == config["admin_user"]

def test_full_database(populated_db_with_all, user_data, product_data):
    """Test that combines multiple fixtures to verify complex state."""
    # Check users
    for user in user_data:
        stored_user = populated_db_with_all.get("users", user["id"])
        assert stored_user == user
    
    # Check products
    for product in product_data:
        stored_product = populated_db_with_all.get("products", product["id"])
        assert stored_product == product

    # Check schema
    schema_info = populated_db_with_all.get("_schemas", "users")
    assert schema_info["owner"] == "admin"