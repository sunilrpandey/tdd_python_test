"""
A simple database client to demonstrate mocking concepts.
"""
import logging
import time
from typing import Dict, Optional

class DatabaseClient:
    """
    A simple database client that demonstrates external dependencies
    that we might want to mock in our tests:
    1. Network connections (simulated with time.sleep)
    2. Logging
    3. External configuration
    4. File operations
    """
    
    def __init__(self, host: str = "localhost", port: int = 5432):
        self.host = host
        self.port = port
        self.connected = False
        self.logger = logging.getLogger(__name__)
        self._data: Dict[str, Dict] = {}  # Simple in-memory storage

    def connect(self) -> bool:
        """Simulate connecting to a database."""
        self.logger.info(f"Connecting to database at {self.host}:{self.port}")
        time.sleep(1)  # Simulate network delay
        self.connected = True
        return True

    def disconnect(self) -> None:
        """Simulate disconnecting from the database."""
        if self.connected:
            self.logger.info("Disconnecting from database")
            time.sleep(0.5)  # Simulate network delay
            self.connected = False

    def get_config(self) -> Dict[str, str]:
        """
        Simulate reading database configuration from a file.
        In real application, this would read from a config file.
        """
        time.sleep(0.1)  # Simulate file read
        return {
            "max_connections": "100",
            "timeout": "30",
            "retry_attempts": "3"
        }

    def execute_query(self, query: str) -> Optional[Dict]:
        """Execute a simulated database query."""
        if not self.connected:
            self.logger.error("Not connected to database")
            return None

        self.logger.debug(f"Executing query: {query}")
        time.sleep(0.2)  # Simulate query execution

        try:
            # Simple query parser for demonstration
            if query.startswith("SELECT"):
                table = query.split("FROM")[1].strip()
                return self._data.get(table, {})
            elif query.startswith("INSERT"):
                # Format: INSERT INTO table_name VALUES name=value
                parts = query.split()
                table = parts[2]
                data = dict(item.split("=") for item in parts[4].split(","))
                if table not in self._data:
                    self._data[table] = {}
                self._data[table][data["id"]] = data
                return data
            else:
                raise ValueError(f"Unsupported query type: {query}")
        except Exception as e:
            self.logger.error(f"Query execution failed: {str(e)}")
            return None

    def backup_data(self, filename: str) -> bool:
        """
        Simulate backing up data to a file.
        In real application, this would write to an actual file.
        """
        if not self.connected:
            self.logger.error("Cannot backup: not connected to database")
            return False

        try:
            self.logger.info(f"Backing up data to {filename}")
            time.sleep(0.5)  # Simulate file write
            return True
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}")
            return False

    def query_with_retry(self, query: str, max_retries: int = 3) -> Optional[Dict]:
        """
        Execute a query with retry logic.
        Demonstrates more complex logic that we might want to test.
        """
        attempts = 0
        while attempts < max_retries:
            try:
                result = self.execute_query(query)
                if result is not None:
                    return result
                attempts += 1
                if attempts < max_retries:
                    self.logger.warning(f"Query failed, retrying ({attempts}/{max_retries})")
                    time.sleep(1)  # Wait before retry
            except Exception as e:
                self.logger.error(f"Error executing query: {str(e)}")
                attempts += 1
                if attempts < max_retries:
                    time.sleep(1)  # Wait before retry

        self.logger.error(f"Query failed after {max_retries} attempts")
        return None