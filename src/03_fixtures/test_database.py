"""
Tests demonstrating pytest fixtures with the Database class.
"""
import pytest
from database import Database

def test_empty_database(db):
    """Test that a new database is empty."""
    assert db.get("users", "1") is None

def test_insert_and_get(db, sample_data):
    """Test inserting and retrieving records."""
    # Insert a record
    db.insert("users", sample_data[0])
    
    # Retrieve the record
    record = db.get("users", "1")
    assert record == sample_data[0]

def test_populated_db(populated_db, sample_data):
    """Test that populated_db fixture contains all sample data."""
    for record in sample_data:
        assert populated_db.get("users", record["id"]) == record

def test_update_record(populated_db):
    """Test updating a record."""
    new_data = {"name": "John Smith"}
    
    # Update record
    success = populated_db.update("users", "1", new_data)
    assert success is True
    
    # Verify update
    record = populated_db.get("users", "1")
    assert record["name"] == "John Smith"
    assert record["email"] == "john@example.com"  # Original email should remain

def test_delete_record(populated_db):
    """Test deleting a record."""
    # Delete record
    success = populated_db.delete("users", "1")
    assert success is True
    
    # Verify deletion
    assert populated_db.get("users", "1") is None

def test_different_tables(db, table_name):
    """Test operations on different tables using parameterized fixture."""
    record = {"id": "1", "data": f"Test data for {table_name}"}
    
    # Insert record
    db.insert(table_name, record)
    
    # Verify record
    assert db.get(table_name, "1") == record

def test_insert_without_id(db):
    """Test that inserting a record without ID raises an error."""
    with pytest.raises(ValueError, match="Record must have an 'id' field"):
        db.insert("users", {"name": "Test User"})