"""
Input handler for ChronoView application.
Handles user input collection and validation.
"""


def get_year():
    """
    Prompt for and validate a year input.
    
    Returns:
        int: A valid year (1-9999)
    """
    while True:
        try:
            year = input("Enter year (1-9999): ")
            year = int(year)
            if 1 <= year <= 9999:
                return year
            else:
                print("Invalid year. Please enter a positive integer (1-9999).")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_month():
    """
    Prompt for and validate a month input.
    
    Returns:
        int: A valid month (1-12)
    """
    while True:
        try:
            month = input("Enter month (1-12): ")
            month = int(month)
            if 1 <= month <= 12:
                return month
            else:
                print("Invalid month. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_first_day_of_week():
    """
    Prompt for and validate the first day of week preference.
    
    Note: This function is kept for reference but is no longer used.
    First day of week is now configured via command-line arguments.
    
    Returns:
        int: 0 for Monday, 6 for Sunday (following calendar module convention)
    """
    while True:
        choice = input("Start week with (M)onday or (S)unday? [M/S]: ").strip().lower()
        if choice == 'm' or choice == 'monday':
            return 0  # Monday (calendar module uses 0 for Monday)
        elif choice == 's' or choice == 'sunday':
            return 6  # Sunday (calendar module uses 6 for Sunday)
        else:
            print("Please enter 'M' for Monday or 'S' for Sunday.")


def validate_input(year, month):
    """
    Validate if the year and month are within acceptable ranges.
    
    Args:
        year (int): Year value to validate
        month (int): Month value to validate
        
    Returns:
        bool: True if both inputs are valid, False otherwise
    """
    valid_year = 1 <= year <= 9999
    valid_month = 1 <= month <= 12
    
    if not valid_year:
        print("Invalid year. Please enter a positive integer (1-9999).")
    if not valid_month:
        print("Invalid month. Please enter a number between 1 and 12.")
        
    return valid_year and valid_month


def get_continue_choice():
    """
    Ask the user if they want to continue using the program.
    
    Returns:
        bool: True if the user wants to continue, False otherwise
    """
    while True:
        choice = input("Would you like to view another calendar? (y/n): ").strip().lower()
        if choice == 'y' or choice == 'yes':
            return True
        elif choice == 'n' or choice == 'no':
            return False
        else:
            print("Please enter 'y' or 'n'.") 