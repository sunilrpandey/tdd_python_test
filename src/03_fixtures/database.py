"""
A simple database simulator to demonstrate pytest fixtures.
"""
from typing import Dict, List, Optional

class Database:
    """Simulates a database with basic CRUD operations."""
    
    def __init__(self):
        """Initialize an empty database."""
        self._data: Dict[str, Dict] = {}
    
    def insert(self, table: str, record: Dict) -> None:
        """Insert a record into a table."""
        if table not in self._data:
            self._data[table] = {}
        
        if "id" not in record:
            raise ValueError("Record must have an 'id' field")
        
        self._data[table][record["id"]] = record.copy()
    
    def get(self, table: str, record_id: str) -> Optional[Dict]:
        """Retrieve a record by ID."""
        return self._data.get(table, {}).get(record_id)
    
    def update(self, table: str, record_id: str, new_data: Dict) -> bool:
        """Update a record by ID."""
        if table not in self._data or record_id not in self._data[table]:
            return False
        
        self._data[table][record_id].update(new_data)
        return True
    
    def delete(self, table: str, record_id: str) -> bool:
        """Delete a record by ID."""
        if table not in self._data or record_id not in self._data[table]:
            return False
        
        del self._data[table][record_id]
        return True
    
    def clear(self) -> None:
        """Clear all data from the database."""
        self._data.clear()