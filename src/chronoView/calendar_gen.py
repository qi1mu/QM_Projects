"""
Calendar generator for ChronoView application.
Handles calendar calculation and formatting.
"""

import calendar
from datetime import datetime


def get_month_name(month):
    """
    Convert month number to month name.
    
    Args:
        month (int): Month number (1-12)
        
    Returns:
        str: Full month name
    """
    month_names = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    return month_names[month - 1]


def format_header(month_name, year):
    """
    Create a centered title with month name and year.
    
    Args:
        month_name (str): Name of the month
        year (int): The year
        
    Returns:
        str: Formatted header string
    """
    title = f"{month_name} {year}"
    return title.center(28)


def format_weekdays(first_day_of_week=0):
    """
    Create a row of weekday abbreviations.
    
    Args:
        first_day_of_week (int): First day of week (0=Monday, 6=Sunday)
        
    Returns:
        str: Formatted weekday header
    """
    # Define all weekday abbreviations
    weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    
    # Reorder based on first day of week
    if first_day_of_week == 6:  # Sunday
        weekdays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
    
    return " ".join(weekdays)


def format_days(year, month, first_day_of_week=0):
    """
    Calculate and format the days in the given month/year.
    
    Args:
        year (int): The year
        month (int): The month (1-12)
        first_day_of_week (int): First day of week (0=Monday, 6=Sunday)
        
    Returns:
        list: List of strings representing weeks in the month
    """
    # Set up the calendar with the appropriate first day of week
    cal = calendar.Calendar(first_day_of_week)
    
    # Get the month calendar
    month_calendar = cal.monthdayscalendar(year, month)
    
    # Format each week
    formatted_weeks = []
    for week in month_calendar:
        week_str = ""
        for day in week:
            if day == 0:
                # Empty space for days not in this month
                week_str += "   "
            else:
                # Right align the day number in a 2-character field
                week_str += f"{day:2d} "
        # Remove trailing space
        week_str = week_str.rstrip()
        formatted_weeks.append(week_str)
    
    return formatted_weeks


def generate_calendar(year, month, first_day_of_week=0):
    """
    Generate a complete calendar for the given month and year.
    
    Args:
        year (int): The year
        month (int): The month (1-12)
        first_day_of_week (int): First day of week (0=Monday, 6=Sunday)
        
    Returns:
        str: Formatted calendar string
    """
    month_name = get_month_name(month)
    header = format_header(month_name, year)
    weekdays = format_weekdays(first_day_of_week)
    days = format_days(year, month, first_day_of_week)
    
    # Combine all components
    calendar_str = f"{header}\n{weekdays}\n"
    calendar_str += "\n".join(days)
    
    return calendar_str


def today_calendar(first_day_of_week=0):
    """
    Generate a calendar for the current month and year.
    
    Args:
        first_day_of_week (int): First day of week (0=Monday, 6=Sunday)
        
    Returns:
        str: Formatted calendar string for current month
    """
    now = datetime.now()
    return generate_calendar(now.year, now.month, first_day_of_week) 