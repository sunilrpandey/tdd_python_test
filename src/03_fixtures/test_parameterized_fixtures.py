"""
This module demonstrates parameterized fixtures in pytest.
"""
import pytest
from database import Database

# Simple parameterized fixture using params
@pytest.fixture(params=[1, 2, 3])
def simple_value(request):
    """
    Basic parameterized fixture that provides different values.
    Each test using this fixture will run once for each parameter.
    """
    return request.param

# Parameterized fixture with ids
@pytest.fixture(params=[
    ("admin", True),
    ("user", False),
    ("guest", False)
], ids=["admin_user", "regular_user", "guest_user"])
def user_role(request):
    """
    Parameterized fixture with custom ids.
    The ids make test output more readable by describing each parameter set.
    """
    return request.param

# Parameterized fixture with complex data
@pytest.fixture(params=[
    {
        "name": "Small Dataset",
        "records": [{"id": "1", "value": "test"}]
    },
    {
        "name": "Medium Dataset",
        "records": [
            {"id": "1", "value": "first"},
            {"id": "2", "value": "second"}
        ]
    },
    {
        "name": "Large Dataset",
        "records": [
            {"id": str(i), "value": f"value{i}"}
            for i in range(1, 4)
        ]
    }
])
def dataset(request):
    """
    Parameterized fixture providing different sized datasets.
    Shows how to use complex data structures as parameters.
    """
    return request.param

# Fixture that combines with parameterized fixture
@pytest.fixture
def populated_test_db(db, dataset):
    """
    Fixture that uses a parameterized fixture.
    Shows how regular fixtures can consume parameterized fixtures.
    """
    for record in dataset["records"]:
        db.insert("test_table", record)
    return db

def test_simple_values(simple_value):
    """Test using a simple parameterized fixture."""
    assert simple_value in [1, 2, 3]

def test_user_permissions(user_role):
    """Test using a parameterized fixture with custom ids."""
    role, is_admin = user_role
    if role == "admin":
        assert is_admin
    else:
        assert not is_admin

def test_dataset_sizes(dataset):
    """Test using a parameterized fixture with complex data."""
    if dataset["name"] == "Small Dataset":
        assert len(dataset["records"]) == 1
    elif dataset["name"] == "Medium Dataset":
        assert len(dataset["records"]) == 2
    else:
        assert len(dataset["records"]) == 3

def test_database_with_datasets(populated_test_db, dataset):
    """Test using a fixture that depends on a parameterized fixture."""
    for record in dataset["records"]:
        stored_record = populated_test_db.get("test_table", record["id"])
        assert stored_record == record

# Example of indirect parameterization
@pytest.mark.parametrize("dataset_name", [
    pytest.param("Small Dataset", id="small"),
    pytest.param("Medium Dataset", id="medium"),
    pytest.param("Large Dataset", id="large")
])
def test_specific_datasets(populated_test_db, dataset, dataset_name):
    """
    Test demonstrating how to combine parameterized fixtures with
    additional parameterization using pytest.mark.parametrize.
    """
    assert dataset["name"] == dataset_name
    records = dataset["records"]
    if dataset_name == "Small Dataset":
        assert len(records) == 1
    elif dataset_name == "Medium Dataset":
        assert len(records) == 2
    else:
        assert len(records) == 3