"""
Test file for Calculator class.
This demonstrates TDD principles.
"""
import pytest
from calculator import Calculator

def test_calculator_creation():
    """Test that we can create a Calculator instance."""
    calc = Calculator()
    assert isinstance(calc, Calculator)

def test_add_two_numbers():
    """Test adding two numbers."""
    calc = Calculator()
    assert calc.add(1, 2) == 3

def test_add_negative_numbers():
    """Test adding negative numbers."""
    calc = Calculator()
    assert calc.add(-1, -2) == -3
    assert calc.add(-1, 2) == 1
    assert calc.add(1, -2) == -1

def test_add_floating_numbers():
    """Test adding floating point numbers."""
    calc = Calculator()
    assert calc.add(1.5, 2.5) == 4.0
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)  # Handle floating point precision

def test_subtract():
    """Test subtraction of two numbers."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(10, 7) == 3
    assert calc.subtract(2, 5) == -3  # Test negative result
    assert calc.subtract(-1, -1) == 0  # Test with negative numbers
    assert calc.subtract(3.5, 2.0) == 1.5  # Test with floating point numbers