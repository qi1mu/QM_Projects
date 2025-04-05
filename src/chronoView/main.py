"""
Main module for ChronoView application.
Controls program flow and user interaction.
"""

import argparse
from src.chronoView.input_handler import get_year, get_month, get_continue_choice, get_first_day_of_week
from src.chronoView.calendar_gen import generate_calendar


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='Terminal-based calendar application')
    parser.add_argument('--start-day', '-s', choices=['monday', 'sunday'], default='monday',
                        help='First day of the week (default: monday)')
    return parser.parse_args()


def get_first_day_value(start_day):
    """
    Convert start day string to calendar module value.
    
    Args:
        start_day (str): First day of week ('monday' or 'sunday')
        
    Returns:
        int: 0 for Monday, 6 for Sunday
    """
    return 0 if start_day.lower() == 'monday' else 6


def display_welcome():
    """Display welcome message."""
    print("\nWelcome to ChronoView!")
    print("A simple terminal calendar application.\n")


def display_goodbye():
    """Display goodbye message."""
    print("\nThank you for using ChronoView. Goodbye!\n")


def run_calendar_loop(first_day_of_week):
    """
    Main program loop for generating calendars.
    
    Args:
        first_day_of_week (int): First day of week (0=Monday, 6=Sunday)
    
    Gets input from user, generates calendars, and handles continuation.
    """
    continue_program = True
    
    while continue_program:
        # Get user input
        year = get_year()
        month = get_month()
        
        # Generate and display calendar
        print("\n" + generate_calendar(year, month, first_day_of_week) + "\n")
        
        # Ask if user wants to continue
        continue_program = get_continue_choice()
    

def main():
    """Main entry point for the application."""
    try:
        args = parse_arguments()
        first_day_of_week = get_first_day_value(args.start_day)
        
        display_welcome()
        print(f"Calendar weeks will start with {args.start_day.capitalize()}.\n")
        run_calendar_loop(first_day_of_week)
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        display_goodbye()


if __name__ == "__main__":
    main() 