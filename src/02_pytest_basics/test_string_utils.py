"""
Tests for StringUtils class demonstrating pytest features.
"""
import pytest
from string_utils import StringUtils

def test_reverse_simple_string():
    """Test basic string reversal."""
    assert StringUtils.reverse("hello") == "olleh"

def test_reverse_empty_string():
    """Test reversing an empty string."""
    assert StringUtils.reverse("") == ""

def test_reverse_invalid_input():
    """Test that reverse() raises TypeError for non-string input."""
    with pytest.raises(TypeError) as exc_info:
        StringUtils.reverse(123)
    assert "Input must be a string" in str(exc_info.value)

def test_is_palindrome_true():
    """Test palindrome detection for valid palindromes."""
    examples = [
        "radar",
        "A man a plan a canal Panama",
        "",  # empty string is a palindrome
        "a",  # single character is a palindrome
    ]
    for text in examples:
        assert StringUtils.is_palindrome(text) is True

def test_is_palindrome_false():
    """Test palindrome detection for non-palindromes."""
    examples = [
        "hello",
        "python",
        "test",
    ]
    for text in examples:
        assert StringUtils.is_palindrome(text) is False

def test_is_palindrome_invalid_input():
    """Test that is_palindrome() raises TypeError for non-string input."""
    with pytest.raises(TypeError, match="Input must be a string"):
        StringUtils.is_palindrome(123)