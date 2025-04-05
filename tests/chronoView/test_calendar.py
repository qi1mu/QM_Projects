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


def test_format_weekdays_monday_start():
    """Test weekday header formatting with Monday as first day."""
    weekdays = format_weekdays(0)  # 0 represents Monday
    assert weekdays == "Mo Tu We Th Fr Sa Su"


def test_format_weekdays_sunday_start():
    """Test weekday header formatting with Sunday as first day."""
    weekdays = format_weekdays(6)  # 6 represents Sunday
    assert weekdays == "Su Mo Tu We Th Fr Sa"


def test_format_days_april_2025_monday_start():
    """Test day formatting for April 2025 with Monday as first day."""
    # April 2025 starts on Tuesday (index 1) with Monday as first day
    days = format_days(2025, 4, 0)  # 0 represents Monday
    # First week should start with empty Monday, then 1-6
    assert "    1  2  3  4  5  6" in days[0]
    # Last week should end on 30 (April has 30 days)
    assert "28 29 30" in days[-1]


def test_format_days_april_2025_sunday_start():
    """Test day formatting for April 2025 with Sunday as first day."""
    # April 2025 with Sunday as first day
    days = format_days(2025, 4, 6)  # 6 represents Sunday
    # First week should have different alignment
    assert "       1  2  3  4  5" in days[0]
    # Last week layout will be different
    assert "27 28 29 30" in days[-1]


def test_generate_calendar_monday_start():
    """Test full calendar generation with Monday as first day."""
    calendar_str = generate_calendar(2025, 4, 0)  # 0 represents Monday
    lines = calendar_str.split("\n")
    
    # Check header
    assert "April 2025" in lines[0]
    
    # Check weekday row
    assert lines[1] == "Mo Tu We Th Fr Sa Su"
    
    # Check first week
    assert "    1  2  3  4  5  6" in lines[2]
    
    # Check that there are at least 5 rows (header, weekdays, 3+ weeks)
    assert len(lines) >= 5


def test_generate_calendar_sunday_start():
    """Test full calendar generation with Sunday as first day."""
    calendar_str = generate_calendar(2025, 4, 6)  # 6 represents Sunday
    lines = calendar_str.split("\n")
    
    # Check header
    assert "April 2025" in lines[0]
    
    # Check weekday row
    assert lines[1] == "Su Mo Tu We Th Fr Sa"
    
    # Check first week (with Sunday as first day)
    assert "       1  2  3  4  5" in lines[2]
    
    # Check that there are at least 5 rows (header, weekdays, 3+ weeks)
    assert len(lines) >= 5


def test_default_parameter_values():
    """Test that default parameter values work correctly."""
    # Default first_day_of_week should be 0 (Monday)
    weekdays_default = format_weekdays()
    weekdays_monday = format_weekdays(0)
    assert weekdays_default == weekdays_monday
    
    # Default in generate_calendar should produce same result as explicit Monday
    cal_default = generate_calendar(2025, 4)
    cal_monday = generate_calendar(2025, 4, 0)
    assert cal_default == cal_monday