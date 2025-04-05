"""
Tests for the input handler module.
"""

import pytest
from unittest.mock import patch
from src.chronoView.input_handler import validate_input


def test_validate_input_valid():
    """Test input validation with valid inputs."""
    assert validate_input(2025, 4) == True
    assert validate_input(1, 1) == True
    assert validate_input(9999, 12) == True


def test_validate_input_invalid_year():
    """Test input validation with invalid year."""
    with patch('builtins.print') as mock_print:
        assert validate_input(0, 4) == False
        assert validate_input(-5, 4) == False
        assert validate_input(10000, 4) == False
        
        # Check that error messages were printed
        mock_print.assert_called()


def test_validate_input_invalid_month():
    """Test input validation with invalid month."""
    with patch('builtins.print') as mock_print:
        assert validate_input(2025, 0) == False
        assert validate_input(2025, 13) == False
        assert validate_input(2025, -1) == False
        
        # Check that error messages were printed
        mock_print.assert_called()


def test_validate_input_both_invalid():
    """Test input validation with both inputs invalid."""
    with patch('builtins.print') as mock_print:
        assert validate_input(0, 0) == False
        assert validate_input(10000, 13) == False
        
        # Check that error messages were printed
        mock_print.assert_called() 