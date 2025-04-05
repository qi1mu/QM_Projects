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


def format_weekdays():
    """
    Create a row of weekday abbreviations.
    
    Returns:
        str: Formatted weekday header
    """
    return "Mo Tu We Th Fr Sa Su"


def format_days(year, month):
    """
    Calculate and format the days in the given month/year.
    
    Args:
        year (int): The year
        month (int): The month (1-12)
        
    Returns:
        list: List of strings representing weeks in the month
    """
    # Create a calendar with Monday as the first day of the week
    cal = calendar.monthcalendar(year, month)
    
    # Format each week
    formatted_weeks = []
    for week in cal:
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


def generate_calendar(year, month):
    """
    Generate a complete calendar for the given month and year.
    
    Args:
        year (int): The year
        month (int): The month (1-12)
        
    Returns:
        str: Formatted calendar string
    """
    month_name = get_month_name(month)
    header = format_header(month_name, year)
    weekdays = format_weekdays()
    days = format_days(year, month)
    
    # Combine all components
    calendar_str = f"{header}\n{weekdays}\n"
    calendar_str += "\n".join(days)
    
    return calendar_str


def today_calendar():
    """
    Generate a calendar for the current month and year.
    
    Returns:
        str: Formatted calendar string for current month
    """
    now = datetime.now()
    return generate_calendar(now.year, now.month) 