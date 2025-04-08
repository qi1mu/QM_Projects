# Wordle Game Design Plan

---

### Project Overview
The goal is to create a terminal-based Wordle game where:
- A random 5-letter word is selected as the target.
- The player has 6 attempts to guess the word.
- Feedback is provided after each guess using distinct symbols:
  - One symbol (e.g., uppercase letter or "*") for a correct letter in the correct position.
  - Another symbol (e.g., lowercase letter or "+") for a correct letter in the wrong position.
  - A third indicator (e.g., "_") for letters not in the word.
- The game runs entirely in the terminal.

---

### Design Plan

#### 1. Functional Requirements
- **Input**:
  - Player enters a 5-letter word as a guess.
  - Input must be validated (exactly 5 letters, alphabetic). Input should be case-insensitive.
- **Output**:
  - Feedback on each guess showing letter correctness with symbols.
  - A win message if the word is guessed correctly within 6 tries.
  - A lose message with the target word if all 6 tries are exhausted.
- **Features**:
  - Randomly select a 5-letter target word from a predefined list stored in a file.
  - Track the number of guesses (up to 6).
  - Display previous guesses and their feedback clearly.
  - Handle invalid inputs with clear error messages without consuming a guess attempt.

#### 2. Program Structure
The program will be organized following the standard project layout defined in the main `README.md`:

```
QM_Projects/
├── docs/
│   └── wordle/
│       └── design_plan.md  # This document
├── src/
│   └── wordle/
│       ├── __init__.py
│       ├── main.py           # Main application script (entry point)
│       ├── word_manager.py   # Handles word list and selection
│       ├── evaluator.py      # Handles guess evaluation and feedback
│       ├── game.py           # Manages the game loop and user interaction
│       └── data/             # Directory for data files
│           └── words.txt     # The list of 5-letter words
└── tests/
    └── wordle/
        ├── __init__.py
        ├── test_word_manager.py
        ├── test_evaluator.py
        └── test_game.py      # Tests for the game logic
```

The core logic will be divided into three main components implemented in separate modules:
- **Word Manager** (`word_manager.py`): Handles the word list and target word selection.
- **Guess Evaluator** (`evaluator.py`): Processes the player's guess and generates feedback.
- **Game Loop/Controller** (`game.py`): Manages the game flow, user interaction, and win/lose conditions.
- **Main Entry Point** (`main.py`): Initializes and starts the game.

#### 3. Detailed Component Design

##### 3.1 Word Manager (`word_manager.py`)
- **Purpose**: Provide and manage the target word.
- **Process**:
  1. Read a list of valid 5-letter words from `src/wordle/data/words.txt`.
  2. Randomly select one word from this list at the start of each game.
  3. Provide the selected target word to the game controller.
- **Considerations**:
  - The word list should contain only 5-letter, alphabetic words.
  - Handle potential file reading errors (e.g., file not found, empty file).

##### 3.2 Guess Evaluator (`evaluator.py`)
- **Purpose**: Compare the player's guess to the target word and provide feedback.
- **Process**:
  1. Take the player's 5-letter guess (normalized to lowercase/uppercase) and the target word.
  2. Implement a two-pass comparison logic:
     - **Pass 1 (Correct Position - `*`)**: Iterate through the guess. If `guess[i] == target[i]`, mark position `i` with `*`. Keep track of target letters used in this pass.
     - **Pass 2 (Wrong Position - `+`)**: Iterate through the guess positions *not* marked with `*`. For `guess[i]`, check if it exists among the *remaining* available letters in the target word (those not matched in Pass 1 and not already used in Pass 2). If yes, mark position `i` with `+` and decrement the count of that available letter in the target.
     - **Incorrect Letter (`_`)**: Any position not marked with `*` or `+` after both passes gets marked with `_`.
  3. Handle duplicate letters correctly via the two-pass approach and tracking available letters.
     - Example: Target `APPLE`, Guess `PEEEL`.
       - Target counts: {A:1, P:2, L:1, E:1}.
       - Pass 1 (`*`): No matches. Feedback: `_____`. Available target letters unchanged.
       - Pass 2 (`+`):
         - Guess 'P' (idx 0): Matches available 'P' in target. Feedback: `+____`. Available target: {A:1, P:1, L:1, E:1}.
         - Guess 'E' (idx 1): Matches available 'E' in target. Feedback: `++___`. Available target: {A:1, P:1, L:1, E:0}.
         - Guess 'E' (idx 2): No available 'E' in target. Feedback: `++___`. Available target: {A:1, P:1, L:1, E:0}.
         - Guess 'E' (idx 3): No available 'E' in target. Feedback: `++___`. Available target: {A:1, P:1, L:1, E:0}.
         - Guess 'L' (idx 4): Matches available 'L' in target. Feedback: `++__+`. Available target: {A:1, P:1, L:0, E:0}.
       - Final Feedback: `++__+`
  4. Return a structured feedback representation (e.g., a list or string like `['+', '+', '_', '_', '+']` or `"++__+"`).
- **Feedback Display**: The `game.py` module will handle formatting this feedback for display.

##### 3.3 Game Loop (`game.py`)
- **Purpose**: Control the game flow and user interaction.
- **Process**:
  1. Initialize the game:
     - Instantiate `WordManager` to get the target word and load the full list of valid words.
     - Set the guess counter to 0 (or remaining guesses to 6).
     - Initialize an empty list to store the history of guesses and their feedback.
  2. Run a loop for up to 6 guesses:
     - Display previous guesses and feedback from the history.
     - Prompt the player to enter a 5-letter word (displaying remaining attempts).
     - Read and normalize the input (e.g., to lowercase).
     - Validate the input:
       - Must be exactly 5 letters.
       - Must be purely alphabetic.
       - **Must exist in the loaded list of valid words.**
       - If invalid, display an error message (e.g., `"Invalid input. Please enter a valid 5-letter word from the dictionary."`) and re-prompt without incrementing the guess counter.
     - If valid, increment the guess counter (or decrement remaining guesses).
     - Pass the guess and target word to the `GuessEvaluator` (`evaluator.py`) to get feedback.
     - Store the guess and its feedback in the history list.
     - Display the latest guess and its feedback.
     - Check win condition: If the feedback indicates a perfect match (e.g., `*****`), end the loop.
  3. End the game:
     - If the player won, display a congratulatory message including the number of guesses taken.
     - If 6 guesses are used without winning, display a "game over" message revealing the target word.
- **Display**: Ensure clear output format for prompts, feedback, history, and final messages.

##### 3.4 Main Entry Point (`main.py`)
- **Purpose**: Launch the application.
- **Process**:
  1. Import necessary classes/functions (e.g., `Game` from `game.py`).
  2. Print a welcome message.
  3. Instantiate the `Game` object.
  4. Call the main method of the `Game` object (e.g., `game.run()`) to start the game loop.
  5. Optionally handle setup like ensuring the `data/words.txt` file exists or catching initialization errors.
  6. Optionally include a "Play Again?" prompt after a game ends.

#### 4. File Content Summary

*   **`docs/wordle/design_plan.md`**: This document. Contains the full design specification.
*   **`src/wordle/__init__.py`**: Marks the directory as a Python package. Empty.
*   **`src/wordle/main.py`**: Entry point. Initializes and starts the `Game`.
*   **`src/wordle/word_manager.py`**: Loads the full word list from `data/words.txt`, validates it, selects the random target word, and provides access to the full list for validation.
*   **`src/wordle/evaluator.py`**: Compares guess to target, generates feedback symbols (`*`, `+`, `_`), handles duplicates using the two-pass method.
*   **`src/wordle/game.py`**: Manages game state, loop, user input/validation (including checking against the valid word list), interaction with other modules, display.
*   **`src/wordle/data/words.txt`**: Plain text list of 5-letter English words (initially ~200-300 common words, one per line). This list will be created during implementation.
*   **`tests/wordle/__init__.py`**: Marks the directory as a Python test package. Empty.
*   **`tests/wordle/test_word_manager.py`**: Pytest tests for word loading, selection, and providing the word list.
*   **`tests/wordle/test_evaluator.py`**: Pytest tests for feedback generation logic, including edge cases and duplicates.
*   **`tests/wordle/test_game.py`**: Pytest tests for game flow, input validation, win/loss conditions.

#### 5. User Interaction Flow
1. Run `python src/wordle/main.py`.
2. See welcome message: "Welcome to Wordle! Guess the 5-letter word in 6 tries."
3. Prompt: "Enter guess 1 (6 remaining): "
4. Player enters guess (e.g., "hello").
5. Input Validation:
   - If invalid (e.g., "hell", "he11o", or "qwert" if "qwert" is not in `words.txt`), show error: `"Invalid input. Please enter a valid 5-letter word from the dictionary."` Re-prompt for guess 1.
   - If valid: Proceed.
6. Evaluate guess using `evaluator.py`.
7. Display result:
   ```
   Guess 1: H E L L O
            _ + * * _
   Enter guess 2 (5 remaining):
   ```
8. Repeat steps 3-7 for up to 6 guesses. Previous guesses are displayed each turn.
9. Game End:
   - Win: "Congratulations! You guessed the word 'WORLD' in 4 guesses!"
   - Lose: "Game Over! You ran out of guesses. The word was 'WORLD'."
10. (Optional) Prompt: "Play again? (y/n): "

#### 6. Output Format Example
- Target word: "FLAME"
- Guess 1: "BREAD" (Assuming BREAD is in words.txt)
  ```
  Guess 1: B R E A D
           _ _ + + _
  Enter guess 2 (5 remaining):
  ```
- Guess 2: "FLAKE" (Assuming FLAKE is in words.txt)
  ```
  Guess 1: B R E A D
           _ _ + + _

  Guess 2: F L A K E
           * * * _ *
  Enter guess 3 (4 remaining):
  ```
- Symbols: `*` = correct position, `+` = wrong position, `_` = not in word.

#### 7. Constraints and Assumptions
- Requires Python 3.x (as per project rules, likely 3.12).
- An initial `data/words.txt` file containing a list of common, valid 5-letter English words will be created and used. File existence and basic format validity should be handled.
- Terminal supports standard text output.
- Input is treated as case-insensitive for comparison but validated against the provided word list.
- Guesses *must* be words present in the `data/words.txt` list.

#### 8. Potential Enhancements (Future Consideration)
- Use a larger, standard word list (e.g., official Scrabble dictionary filtered for 5-letter words).
- Implement colored terminal output (e.g., green for `*`, yellow for `+`, grey for `_`) using a library like `rich` or `colorama`.
- Add difficulty levels (e.g., changing word length or number of guesses).
- Track player statistics (win rate, guess distribution).
- Add ability to share results (like the classic Wordle squares).
- Implement the "Play Again?" feature.

### Gameplay Mechanics

*   **Guess Input:** The player enters a 5-letter word.
*   **Input Validation:**
    *   Check if the input is exactly 5 letters long.
    *   Check if the input consists only of alphabetic characters.
    *   Check if the input word exists in the allowed guess list (`WordManager.is_valid_word`).
    *   If invalid, provide specific feedback and re-prompt.
*   **Guess Evaluation:** (`Evaluator.evaluate_guess`)
    *   Compare the guess against the target word.
    *   Generate feedback symbols (`*`, `+`, `_`) for each letter.
*   **Feedback Display:**
    *   Show the guess history, including the feedback for each guess.
    *   Ensure feedback symbols align correctly under the corresponding letters.
*   **Win Condition:** The player guesses the target word correctly within the allowed number of guesses for the chosen difficulty.
*   **Lose Condition:** The player uses all allowed guesses without guessing the word.
*   **Hint System:**
    *   **Activation:** Player types "hint" (case-insensitive) instead of a guess.
    *   **Availability:** Dependent on difficulty level (see above). Tracked via `hints_used_count`.
    *   **Limit:** Number of hints allowed varies by difficulty.
    *   **Functionality:** Reveals one letter that is in the correct position but has not yet been marked with '*' in that specific position in any previous guess. If multiple such letters exist, one is chosen randomly.
    *   **Feedback:** Informs the player if hints are disabled, if they have used all available hints, or provides the hint.

### Game Flow

---

## Usage

Run the game from the project root directory using Python:

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

Type "hint" (if available for your difficulty) during your turn to use a hint.

---

This updated design plan incorporates the agreed-upon file structure and details the purpose of each file. 

## Features

*   Standard Wordle gameplay: Guess a 5-letter hidden word.
*   **Difficulty Levels:** Configurable via `--level` command-line argument (`easy`, `medium` (default), `hard`, `pro`).
    *   **Easy:** 8 guesses, 2 hints.
    *   **Medium:** 6 guesses, 1 hint.
    *   **Hard:** 6 guesses, 0 hints.
    *   **Pro:** 5 guesses, 0 hints.
*   Feedback symbols:
    *   `*`: Correct letter in the correct position.
    *   `+`: Correct letter in the wrong position.
    *   `_`: Incorrect letter.
    *   Show the guess history, including the feedback for each guess.
    *   Ensure feedback symbols align correctly under the corresponding letters.
*   **Win Condition:** The player guesses the target word correctly within the allowed number of guesses for the chosen difficulty.
*   **Lose Condition:** The player uses all allowed guesses without guessing the word.
*   **Hint System:**
    *   **Activation:** Player types "hint" (case-insensitive) instead of a guess.
    *   **Availability:** Dependent on difficulty level (see above). Tracked via `hints_used_count`.
    *   **Limit:** Number of hints allowed varies by difficulty.
    *   **Functionality:** Reveals one letter that is in the correct position but has not yet been marked with '*' in that specific position in any previous guess. If multiple such letters exist, one is chosen randomly.
    *   **Feedback:** Informs the player if hints are disabled, if they have used all available hints, or provides the hint.

### Game Flow

---

This updated design plan incorporates the agreed-upon file structure and details the purpose of each file. 