"""
Simple database module with external dependencies for demonstrating mocking.
"""
import time
import logging
from datetime import datetime

class DatabaseConnection:
    """Simulates a database connection with external dependencies."""
    
    def __init__(self, host="localhost", port=5432):
        self.host = host
        self.port = port
        self.connected = False
        self._logger = logging.getLogger(__name__)

    def connect(self):
        """Simulate connecting to a database."""
        # Simulating network delay
        time.sleep(1)  # This is what we'll want to mock
        self.connected = True
        self._logger.info(f"Connected to database at {self.host}:{self.port}")
        return self.connected

    def disconnect(self):
        """Simulate disconnecting from a database."""
        if self.connected:
            # Simulate cleanup delay
            time.sleep(0.5)  # This is what we'll want to mock
            self.connected = False
            self._logger.info("Disconnected from database")

class Database:
    """Main database class that we'll use to demonstrate different mocking techniques."""
    
    def __init__(self, connection):
        self.connection = connection
        self._data = {}
        self._logger = logging.getLogger(__name__)

    def insert(self, table: str, record: dict) -> bool:
        """Insert a record into a table."""
        try:
            if not self.connection.connected:
                raise RuntimeError("Not connected to database")
            
            if table not in self._data:
                self._data[table] = {}
            
            if "id" not in record:
                raise ValueError("Record must have an 'id' field")
            
            # Simulate write delay
            time.sleep(0.1)  # This is what we'll want to mock
            
            record_id = record["id"]
            self._data[table][record_id] = {
                **record,
                "created_at": datetime.now()
            }
            
            self._logger.debug(f"Inserted record {record_id} into {table}")
            return True
            
        except Exception as e:
            self._logger.error(f"Error inserting record: {str(e)}")
            return False

    def get(self, table: str, record_id: str) -> dict:
        """Retrieve a record from a table."""
        try:
            if not self.connection.connected:
                raise RuntimeError("Not connected to database")
            
            # Simulate read delay
            time.sleep(0.05)  # This is what we'll want to mock
            
            return self._data.get(table, {}).get(record_id)
            
        except Exception as e:
            self._logger.error(f"Error retrieving record: {str(e)}")
            return None

    def update(self, table: str, record_id: str, new_data: dict) -> bool:
        """Update a record in a table."""
        try:
            if not self.connection.connected:
                raise RuntimeError("Not connected to database")
            
            if table not in self._data or record_id not in self._data[table]:
                return False
            
            # Simulate update delay
            time.sleep(0.1)  # This is what we'll want to mock
            
            self._data[table][record_id].update(new_data)
            self._data[table][record_id]["updated_at"] = datetime.now()
            
            self._logger.debug(f"Updated record {record_id} in {table}")
            return True
            
        except Exception as e:
            self._logger.error(f"Error updating record: {str(e)}")
            return False

    def delete(self, table: str, record_id: str) -> bool:
        """Delete a record from a table."""
        try:
            if not self.connection.connected:
                raise RuntimeError("Not connected to database")
            
            if table not in self._data or record_id not in self._data[table]:
                return False
            
            # Simulate delete delay
            time.sleep(0.1)  # This is what we'll want to mock
            
            del self._data[table][record_id]
            self._logger.debug(f"Deleted record {record_id} from {table}")
            return True
            
        except Exception as e:
            self._logger.error(f"Error deleting record: {str(e)}")
            return False