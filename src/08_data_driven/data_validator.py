"""
Data validator demonstrating data-driven testing.
"""
import re
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class User:
    """User data model with validation."""
    name: str
    age: int
    email: str
    
    def is_valid(self) -> bool:
        """Validate user data."""
        # Validate name
        if not self.name or not isinstance(self.name, str):
            return False
        
        # Validate age
        if not isinstance(self.age, (int, float)) or self.age <= 18 or self.age >= 100:
            return False
        
        # Validate email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            return False
        
        return True

@dataclass
class Product:
    """Product data model with validation."""
    id: str
    name: str
    price: float
    stock: int
    
    def is_valid(self) -> bool:
        """Validate product data."""
        if not self.id or not isinstance(self.id, str):
            return False
        
        if not self.name or not isinstance(self.name, str):
            return False
        
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            return False
        
        if not isinstance(self.stock, int) or self.stock < 0:
            return False
        
        return True

class DataValidator:
    """Utility class for data validation."""
    
    @staticmethod
    def validate_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """Validate date string format."""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format."""
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_card_number(card_number: str) -> bool:
        """
        Validate credit card number using Luhn algorithm.
        """
        if not card_number.isdigit():
            return False
        
        # Luhn algorithm
        digits = [int(d) for d in card_number]
        checksum = digits.pop()
        digits.reverse()
        
        processed_digits = []
        for i, digit in enumerate(digits):
            if i % 2 == 0:
                doubled = digit * 2
                if doubled > 9:
                    doubled -= 9
                processed_digits.append(doubled)
            else:
                processed_digits.append(digit)
        
        total = sum(processed_digits) + checksum
        return total % 10 == 0
    
    @staticmethod
    def validate_dict(data: Dict[str, Any], required_fields: Dict[str, type]) -> bool:
        """Validate dictionary against required fields and types."""
        for field, field_type in required_fields.items():
            if field not in data:
                return False
            if not isinstance(data[field], field_type):
                return False
        return True