"""
Tests for command-line argument parsing in the main module.
"""

import pytest
from unittest.mock import patch
import argparse
from src.chronoView.main import parse_arguments, get_first_day_value


def test_parse_arguments_default():
    """Test that default arguments are correctly set."""
    with patch('argparse.ArgumentParser.parse_args',
               return_value=argparse.Namespace(start_day='monday')):
        args = parse_arguments()
        assert args.start_day == 'monday'


def test_parse_arguments_sunday():
    """Test that sunday argument is correctly parsed."""
    with patch('argparse.ArgumentParser.parse_args',
               return_value=argparse.Namespace(start_day='sunday')):
        args = parse_arguments()
        assert args.start_day == 'sunday'


def test_get_first_day_value_monday():
    """Test conversion of 'monday' to calendar value."""
    assert get_first_day_value('monday') == 0
    assert get_first_day_value('Monday') == 0
    assert get_first_day_value('MONDAY') == 0


def test_get_first_day_value_sunday():
    """Test conversion of 'sunday' to calendar value."""
    assert get_first_day_value('sunday') == 6
    assert get_first_day_value('Sunday') == 6
    assert get_first_day_value('SUNDAY') == 6 