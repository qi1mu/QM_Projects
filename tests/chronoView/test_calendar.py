"""
Tests for the calendar generator module.
"""

import pytest
from src.chronoView.calendar_gen import (
    get_month_name,
    format_header,
    format_weekdays,
    format_days,
    generate_calendar
)


def test_get_month_name():
    """Test month number to name conversion."""
    assert get_month_name(1) == "January"
    assert get_month_name(4) == "April"
    assert get_month_name(12) == "December"


def test_format_header():
    """Test header formatting."""
    header = format_header("April", 2025)
    assert "April 2025" in header
    assert len(header) == 28  # Check if centered in 28-char field


def test_format_weekdays():
    """Test weekday header formatting."""
    weekdays = format_weekdays()
    assert weekdays == "Mo Tu We Th Fr Sa Su"


def test_format_days_april_2025():
    """Test day formatting for April 2025."""
    # April 2025 starts on Tuesday (index 1)
    days = format_days(2025, 4)
    # First week should start with empty Monday, then 1-6
    assert "    1  2  3  4  5  6" in days[0]
    # Last week should end on 30 (April has 30 days)
    assert "28 29 30" in days[-1]


def test_generate_calendar():
    """Test full calendar generation."""
    calendar_str = generate_calendar(2025, 4)
    lines = calendar_str.split("\n")
    
    # Check header
    assert "April 2025" in lines[0]
    
    # Check weekday row
    assert lines[1] == "Mo Tu We Th Fr Sa Su"
    
    # Check first week
    assert "    1  2  3  4  5  6" in lines[2]
    
    # Check that there are at least 5 rows (header, weekdays, 3+ weeks)
    assert len(lines) >= 5 