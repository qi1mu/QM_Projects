# ChronoView: Terminal Calendar Application

## Project Overview

ChronoView is a simple terminal-based calendar application that allows users to view monthly calendars for any specified month and year. The application runs entirely in the terminal without requiring a graphical interface.

## Features

- Display a formatted calendar for any month of any year
- Accept user input for month (1-12) and year
- Format calendar output with days aligned under weekday headers
- Show month name and year as a header
- Handle invalid inputs with appropriate error messages
- Allow users to generate multiple calendars in one session

## Technical Design

### Project Structure

```
chronoview/
│
├── docs/
│   └── calendar_design.md
│
├── src/
│   ├── __init__.py
│   ├── main.py           # Main program entry point
│   ├── input_handler.py  # Handle and validate user input
│   └── calendar_gen.py   # Generate and format calendars
│
├── tests/
│   ├── __init__.py
│   ├── test_input.py
│   └── test_calendar.py
│
├── requirements.txt      # Minimal dependencies
└── README.md            # Project instructions and overview
```

### Component Design

#### 1. Input Handler (`input_handler.py`)

**Purpose**: Collect and validate user input for year and month.

**Main Functions**:
- `get_year()`: Prompt for and validate a year input
- `get_month()`: Prompt for and validate a month input
- `validate_input(year, month)`: Check if inputs are within valid ranges

**Validation Rules**:
- Year must be a positive integer (1-9999)
- Month must be an integer between 1 and 12
- Non-numeric inputs are rejected with appropriate error messages

#### 2. Calendar Generator (`calendar_gen.py`)

**Purpose**: Calculate and format calendar output for a given month and year.

**Main Functions**:
- `generate_calendar(year, month)`: Create a formatted calendar string
- `get_month_name(month)`: Convert month number to name
- `format_header(month_name, year)`: Create centered title
- `format_weekdays()`: Create row of weekday abbreviations
- `format_days(year, month)`: Calculate and format days into weeks

**Implementation Details**:
- Will utilize Python's built-in `calendar` module
- Calendar will be formatted with days of the week from Monday to Sunday
- Days will be right-aligned in fixed-width spaces
- Spaces will be left blank for days not in the specified month

#### 3. Main Program (`main.py`)

**Purpose**: Control program flow and user interaction.

**Main Functions**:
- `main()`: Program entry point
- `run_calendar_loop()`: Handle repeat calendar generation
- `display_welcome()`: Show welcome message
- `display_goodbye()`: Show exit message

**Program Flow**:
1. Display welcome message
2. Enter main loop:
   - Get valid year and month from input handler
   - Generate and display calendar
   - Ask if user wants another calendar
   - Exit or repeat based on response
3. Display goodbye message on exit

### Dependencies

The application will have minimal external dependencies:
- Python 3.6+ (for f-strings and modern calendar module features)
- Standard library modules only (calendar, datetime)

## User Interface

### Input Prompts

```
Welcome to ChronoView!
Enter year (1-9999): 2025
Enter month (1-12): 4
```

### Output Format

```
           April 2025           
Mo Tu We Th Fr Sa Su
    1  2  3  4  5  6
 7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30
```

### Error Messages

```
Invalid year. Please enter a positive integer (1-9999).
Invalid month. Please enter a number between 1 and 12.
```

### Continuation Prompt

```
Would you like to view another calendar? (y/n): 
```

## Future Enhancements

Potential future improvements:
- Color-coding for better readability
- Highlighting current day when viewing the current month
- Adding event marking/tracking capabilities
- Supporting different calendar display formats (e.g., year view)
- Command-line arguments for non-interactive use
- Adding national holidays or observances

## Testing Strategy

Testing will focus on:
1. Input validation (handling various edge cases)
2. Calendar generation correctness (particularly for leap years)
3. Proper formatting of different length months
4. Program flow and user interaction

Unit tests will be created for all major components, with particular attention to edge cases such as leap years, months with 31 days, and various starting weekdays. 