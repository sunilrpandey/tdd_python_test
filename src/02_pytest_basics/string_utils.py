"""
String utility functions to demonstrate pytest features.
"""

class StringUtils:
    """A class containing string utility functions."""
    
    @staticmethod
    def reverse(text: str) -> str:
        """Reverse a string."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        return text[::-1]
    
    @staticmethod
    def is_palindrome(text: str) -> bool:
        """Check if a string is a palindrome."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        # Remove spaces and convert to lowercase
        text = text.replace(" ", "").lower()
        return text == text[::-1]
    
    