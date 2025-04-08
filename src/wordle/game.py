import random # Added for hint selection
from .word_manager import WordManager
from .evaluator import Evaluator

class Game:
    """Manages the Wordle game loop, state, and user interaction.

    Handles different difficulty levels affecting guesses and hints.
    """

    # Default values (will be overridden based on difficulty)
    MAX_GUESSES = 6
    ALLOWED_HINTS = 1

    def __init__(self, difficulty="medium"):
        """Initializes the game components based on the chosen difficulty."""
        self.difficulty = difficulty.lower() # Store difficulty

        # Set rules based on difficulty
        if self.difficulty == "easy":
            self.MAX_GUESSES = 8
            self.ALLOWED_HINTS = 2
        elif self.difficulty == "medium":
            self.MAX_GUESSES = 6
            self.ALLOWED_HINTS = 1
        elif self.difficulty == "hard":
            self.MAX_GUESSES = 6
            self.ALLOWED_HINTS = 0 # No hints for hard
        elif self.difficulty == "pro":
            self.MAX_GUESSES = 5
            self.ALLOWED_HINTS = 0 # No hints for pro
        else:
            # Fallback to medium if somehow an invalid difficulty is passed
            print(f"Warning: Invalid difficulty '{self.difficulty}' received. Defaulting to Medium.")
            self.difficulty = "medium"
            self.MAX_GUESSES = 6
            self.ALLOWED_HINTS = 1

        try:
            self.word_manager = WordManager() # Assumes words.txt is in default location
            self.evaluator = Evaluator()
            self.target_word = self.word_manager.get_target_word()
            self.guesses_history = [] # Stores tuples of (guess, feedback_list)
            self.remaining_guesses = self.MAX_GUESSES
            # self.hint_used = False # Replaced by hints_used_count
            self.hints_used_count = 0 # Track hints used
        except ValueError as e:
            print(f"Error initializing game: {e}")
            self.target_word = None # Prevent game from running if setup fails

    def _display_welcome(self):
        """Displays the welcome message including difficulty info."""
        print("\nWelcome to Wordle!")
        print(f"Difficulty: {self.difficulty.capitalize()}")
        print(f"Guess the 5-letter word in {self.MAX_GUESSES} tries.")
        if self.ALLOWED_HINTS > 0:
            plural = "s" if self.ALLOWED_HINTS > 1 else ""
            print(f"You have {self.ALLOWED_HINTS} hint{plural} available (type 'hint').")
        else:
            print("Hints are disabled for this difficulty.")
        print("Feedback symbols: '*' = Correct position, '+' = Wrong position, '_' = Incorrect letter")

    def _display_history(self):
        """Displays the history of guesses and feedback."""
        if not self.guesses_history:
            return
        print("\n--- Guesses So Far ---")
        for i, (guess, feedback) in enumerate(self.guesses_history):
            feedback_str = " ".join(feedback)
            guess_str = " ".join(list(guess.upper()))
            # Calculate dynamic padding based on the prefix length
            prefix = f"Guess {i+1}: "
            padding = " " * len(prefix)
            print(f"{prefix}{guess_str}")
            print(f"{padding}{feedback_str}") # Apply dynamic padding
        print("----------------------")

    def _provide_hint(self):
        """Provides a hint to the player by revealing one correctly placed letter
           that hasn't been revealed yet. Sets the hint_used flag."""
        if not self.target_word: return # Should not happen if game is running

        known_correct_positions = [False] * len(self.target_word)
        for _, feedback in self.guesses_history:
            for i, symbol in enumerate(feedback):
                if symbol == self.evaluator.CORRECT_POSITION:
                    known_correct_positions[i] = True

        available_hint_indices = [
            i for i, known in enumerate(known_correct_positions)
            if not known
        ]

        if not available_hint_indices:
            print("Hint: No further positional hints available (all correct letters' positions known).")
        else:
            hint_index = random.choice(available_hint_indices)
            hint_letter = self.target_word[hint_index]
            print(f"Hint: The letter in position {hint_index + 1} is '{hint_letter.upper()}'.")
            # self.hint_used = True # Replaced by hints_used_count
            self.hints_used_count += 1 # Increment hints used count

    def _get_user_guess(self):
        """Prompts the user for a guess, handles 'hint' requests, and validates the guess."""
        while True:
            hints_remaining = self.ALLOWED_HINTS - self.hints_used_count
            prompt = f"\nEnter guess {self.MAX_GUESSES - self.remaining_guesses + 1} "
            prompt += f"({self.remaining_guesses} remaining" 
            if self.ALLOWED_HINTS > 0:
                 plural = "s" if hints_remaining != 1 else ""
                 prompt += f", {hints_remaining} hint{plural} left): " 
            else:
                 prompt += "): "

            raw_input = input(prompt).strip()
            guess = raw_input.lower()

            if guess == "hint":
                if self.ALLOWED_HINTS == 0:
                    print("Hints are disabled for this difficulty level.")
                elif self.hints_used_count >= self.ALLOWED_HINTS:
                    print("You have already used all your hints for this game.")
                else:
                    self._provide_hint()
                continue # Always re-prompt after hint attempt (success or fail)

            if len(guess) != 5:
                print("Invalid input. Guess must be exactly 5 letters long.")
                continue
            if not guess.isalpha():
                print("Invalid input. Guess must contain only letters.")
                continue
            if not self.word_manager.is_valid_word(guess):
                print("Invalid input. Please enter a valid 5-letter word from the dictionary.")
                continue

            return guess # Valid guess received

    def _display_result(self, win):
        """Displays the final win or lose message."""
        print("\n======================")
        if win:
            guesses_taken = self.MAX_GUESSES - self.remaining_guesses + 1
            print(f"Congratulations! You guessed the word '{self.target_word.upper()}' in {guesses_taken} guesses!")
        else:
            print(f"Game Over! You ran out of guesses.")
            print(f"The word was: '{self.target_word.upper()}'")
        print("======================")

    def run(self):
        """Runs the main game loop."""
        if not self.target_word:
            print("Cannot start game due to initialization error.")
            return # Exit if setup failed

        self._display_welcome()
        win = False

        while self.remaining_guesses > 0:
            self._display_history()
            guess = self._get_user_guess()
            feedback = self.evaluator.evaluate_guess(self.target_word, guess)
            self.guesses_history.append((guess, feedback))
            self.remaining_guesses -= 1

            # Display the latest guess immediately with correct alignment
            guess_display_str = " ".join(list(guess.upper()))
            feedback_display_str = " ".join(feedback)
            # Calculate dynamic padding based on the prefix length
            prefix = f"Guess {self.MAX_GUESSES - self.remaining_guesses}: "
            padding = " " * len(prefix)
            print(f"{prefix}{guess_display_str}")
            print(f"{padding}{feedback_display_str}") # Apply dynamic padding

            if feedback == [self.evaluator.CORRECT_POSITION] * 5:
                win = True
                break # Exit loop on win

        self._display_result(win)

        # Optional: Add play again logic here later

# Note: This file is intended to be run via main.py, not directly.
# No __main__ block here. 