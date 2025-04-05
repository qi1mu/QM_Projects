"""
Main module for ChronoView application.
Controls program flow and user interaction.
"""

from src.chronoView.input_handler import get_year, get_month, get_continue_choice
from src.chronoView.calendar_gen import generate_calendar


def display_welcome():
    """Display welcome message."""
    print("\nWelcome to ChronoView!")
    print("A simple terminal calendar application.\n")


def display_goodbye():
    """Display goodbye message."""
    print("\nThank you for using ChronoView. Goodbye!\n")


def run_calendar_loop():
    """
    Main program loop for generating calendars.
    
    Gets input from user, generates calendars, and handles continuation.
    """
    continue_program = True
    
    while continue_program:
        # Get user input
        year = get_year()
        month = get_month()
        
        # Generate and display calendar
        print("\n" + generate_calendar(year, month) + "\n")
        
        # Ask if user wants to continue
        continue_program = get_continue_choice()
    

def main():
    """Main entry point for the application."""
    try:
        display_welcome()
        run_calendar_loop()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        display_goodbye()


if __name__ == "__main__":
    main() 