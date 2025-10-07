"""
Shared fixtures for database tests.
"""
import pytest
from database import Database

@pytest.fixture(scope="function")
def db():
    """Create a new database instance for each test."""
    database = Database()
    yield database
    database.clear()

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return [
        {"id": "1", "name": "John Doe", "email": "john@example.com"},
        {"id": "2", "name": "Jane Smith", "email": "jane@example.com"},
        {"id": "3", "name": "Bob Johnson", "email": "bob@example.com"},
    ]

@pytest.fixture
def populated_db(db, sample_data):
    """Provide a database populated with sample data."""
    for record in sample_data:
        db.insert("users", record)
    return db

@pytest.fixture(params=["users", "products", "orders"])
def table_name(request):
    """Parameterized fixture providing different table names."""
    return request.param