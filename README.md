# QM_Projects

A collection of Python and JavaScript projects for practicing coding with AI assistance. This repository contains various games and terminal applications.

## Implemented Projects

1.  **ChronoView:** A terminal-based calendar application (details below).
2.  **Wordle:** A terminal-based implementation of the popular word-guessing game (details below).

## Project Structure

```
QM_Projects/
└── ...
    ├── docs/
    │   └── chronoView/
    │       └── calendar_design.md
    ├── src/
    │   └── chronoView/
    │       ├── __init__.py
    │       ├── main.py         # Main application script
    │       ├── input_handler.py
    │       └── calendar_gen.py
    └── tests/
        └── chronoView/
            └── ... # Test files for chronoView
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
1. Choose a project from the `src/` directory (e.g., `src/chronoView`)
2. Follow the specific README instructions in each project folder (if available)
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
python src/chronoView/main.py
```

Follow the prompts to:
1. Enter a year (1-9999)
2. Enter a month (1-12)

The application will display a calendar for the specified month and year, then ask if you want to view another calendar.

## Example output:
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
QM_Projects/
│
├── docs/
│   └── chronoView/
│       └── calendar_design.md
│
├── src/
│   └── chronoView/
│       ├── __init__.py
│       ├── main.py
│       ├── input_handler.py
│       └── calendar_gen.py
└── tests/
    └── chronoView/
        └── ... # Test files for chronoView
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

---

# Wordle

A terminal-based implementation of the classic word-guessing game.

## Features

- Standard Wordle gameplay: Guess a 5-letter hidden word in 6 tries.
- Feedback symbols:
    - `*`: Correct letter in the correct position.
    - `+`: Correct letter in the wrong position.
    - `_`: Incorrect letter.
- Validates guesses against a dictionary of 5-letter words.
- Hint system: Allows the player to request one hint per game to reveal a correct letter/position.
- Clear terminal display with aligned feedback.

## Usage

Run the game using Python:

```bash
# Run with default (Medium) difficulty
python src/wordle/main.py

# Run with a specific difficulty
python src/wordle/main.py --level easy
python src/wordle/main.py --level hard
python src/wordle/main.py -l pro # Short flag also works
```

Available difficulty levels:
- `easy`: 8 guesses, 2 hints
- `medium`: 6 guesses, 1 hint (Default)
- `hard`: 6 guesses, 0 hints
- `pro`: 5 guesses, 0 hints

Follow the prompts to enter your guesses. Type "hint" (if available for your difficulty) to use a hint.

## Project Structure

```
QM_Projects/
│
├── docs/
│   └── wordle/
│       └── design_plan.md
│
├── src/
│   └── wordle/
│       ├── __init__.py
│       ├── main.py
│       ├── word_manager.py
│       ├── evaluator.py
│       ├── game.py
│       └── data/
│           └── words.txt
└── tests/
    └── wordle/
        ├── __init__.py
        ├── test_evaluator.py
        └── test_word_manager.py
```
