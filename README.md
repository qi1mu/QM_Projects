# QM_Projects

A collection of Python and JavaScript projects for practicing coding with AI assistance. This repository contains various games and terminal applications.

## Project Structure

```
QM_Projects/
├── src/
│   ├── python/
│   │   ├── games/      # Python-based games
│   │   ├── terminal_apps/  # Terminal-based applications
│   │   └── utils/      # Utility functions and helpers
│   └── web/
│       ├── js/         # JavaScript files
│       ├── css/        # Stylesheets
│       └── html/       # HTML templates
├── tests/              # Test files
├── docs/              # Documentation
└── examples/          # Example implementations
```

## Setup Instructions

### Python Environment
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate  # On Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### JavaScript Environment
1. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Getting Started
1. Choose a project from the `src/python/games` or `src/python/terminal_apps` directory
2. Follow the specific README instructions in each project folder
3. Run the project using the provided instructions

## Contributing
Feel free to add your own projects or improve existing ones. Please follow these guidelines:
1. Create a new branch for your feature
2. Add appropriate documentation
3. Include tests for your code
4. Submit a pull request

## License
This project is open source and available under the MIT License.

# ChronoView

A simple terminal-based calendar application that allows users to view a formatted calendar for any month of any year.

## Features

- Display a formatted calendar for any month of any year
- Clean, readable terminal output
- Input validation and error handling
- Simple and intuitive user interface

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-folder>
   ```

2. No external dependencies required - ChronoView only uses Python's standard library.

## Usage

Run the application using Python:

```
python src/run_chronoview.py
```

Follow the prompts to:
1. Enter a year (1-9999)
2. Enter a month (1-12)

The application will display a calendar for the specified month and year, then ask if you want to view another calendar.

Example output:
```
        April 2025        
Mo Tu We Th Fr Sa Su
    1  2  3  4  5  6
 7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30
```

## Project Structure

```
chronoview/
│
├── docs/
│   └── chronoView/
│       └── calendar_design.md
│
├── src/
│   ├── chronoView/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── input_handler.py
│   │   └── calendar_gen.py
│   └── run_chronoview.py
│
└── README.md
```

## License

[License information]

## Contributing

Contributions to ChronoView are welcome! Please feel free to submit a Pull Request.

## Future Enhancements

- Add color coding for better readability
- Highlight the current day when viewing the current month
- Add support for different starting days of the week (Monday/Sunday)
- Command-line arguments for non-interactive use
