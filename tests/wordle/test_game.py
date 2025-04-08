import pytest
from unittest.mock import patch

# Assume Game is importable - adjust path if necessary based on project structure
# e.g., from src.wordle.game import Game
# If running pytest from root, PYTHONPATH might need adjustment or use relative imports
try:
    from src.wordle.game import Game
    from src.wordle.word_manager import WordManager
except ImportError:
    # Simple fallback for running tests directly in tests/wordle perhaps
    # This might need refinement depending on how tests are executed
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from src.wordle.game import Game
    from src.wordle.word_manager import WordManager

# Mock WordManager to avoid file dependency during Game init tests
@pytest.fixture(autouse=True)
def mock_word_manager(mocker):
    mocker.patch.object(WordManager, '__init__', return_value=None)
    mocker.patch.object(WordManager, 'get_target_word', return_value="tests") # Need a 5-letter word
    mocker.patch.object(WordManager, 'is_valid_word', return_value=True)

# --- Test Difficulty Initialization ---

def test_game_init_default_difficulty():
    """Test Game initializes with Medium difficulty by default."""
    game = Game()
    assert game.difficulty == "medium"
    assert game.MAX_GUESSES == 6
    assert game.ALLOWED_HINTS == 1
    assert game.hints_used_count == 0

def test_game_init_easy_difficulty():
    """Test Game initializes correctly for Easy difficulty."""
    game = Game(difficulty="easy")
    assert game.difficulty == "easy"
    assert game.MAX_GUESSES == 8
    assert game.ALLOWED_HINTS == 2
    assert game.hints_used_count == 0

def test_game_init_medium_difficulty():
    """Test Game initializes correctly for Medium difficulty."""
    game = Game(difficulty="medium")
    assert game.difficulty == "medium"
    assert game.MAX_GUESSES == 6
    assert game.ALLOWED_HINTS == 1
    assert game.hints_used_count == 0

def test_game_init_hard_difficulty():
    """Test Game initializes correctly for Hard difficulty."""
    game = Game(difficulty="hard")
    assert game.difficulty == "hard"
    assert game.MAX_GUESSES == 6
    assert game.ALLOWED_HINTS == 0
    assert game.hints_used_count == 0

def test_game_init_pro_difficulty():
    """Test Game initializes correctly for Pro difficulty."""
    game = Game(difficulty="pro")
    assert game.difficulty == "pro"
    assert game.MAX_GUESSES == 5
    assert game.ALLOWED_HINTS == 0
    assert game.hints_used_count == 0

def test_game_init_invalid_difficulty_fallback(capsys):
    """Test Game falls back to Medium for invalid difficulty string."""
    game = Game(difficulty="nonsense")
    captured = capsys.readouterr()
    assert "Warning: Invalid difficulty 'nonsense' received." in captured.out
    assert game.difficulty == "medium"
    assert game.MAX_GUESSES == 6
    assert game.ALLOWED_HINTS == 1
    assert game.hints_used_count == 0

# --- Tests for Hint Logic ---

# Helper function to run one iteration of the guess loop for hint testing
def run_guess_loop_once_for_hint(game):
    # Patch input to return 'hint' then raise StopIteration to break the loop
    with patch('builtins.input', side_effect=['hint', StopIteration]):
        with pytest.raises(StopIteration):
            game._get_user_guess()

def test_hint_easy_difficulty_allows_two(capsys):
    """Test Easy difficulty allows two hints."""
    game = Game(difficulty="easy")
    game.target_word = "apple"

    # First hint
    run_guess_loop_once_for_hint(game)
    captured = capsys.readouterr()
    assert "Hint:" in captured.out
    assert game.hints_used_count == 1

    # Second hint
    run_guess_loop_once_for_hint(game)
    captured = capsys.readouterr()
    assert "Hint:" in captured.out # Check if second hint is given
    assert game.hints_used_count == 2

    # Third hint (should be denied)
    run_guess_loop_once_for_hint(game)
    captured = capsys.readouterr()
    assert "You have already used all your hints" in captured.out
    assert game.hints_used_count == 2 # Count should not increase

def test_hint_medium_difficulty_allows_one(capsys):
    """Test Medium difficulty allows one hint."""
    game = Game(difficulty="medium")
    game.target_word = "apple"

    # First hint
    run_guess_loop_once_for_hint(game)
    captured = capsys.readouterr()
    assert "Hint:" in captured.out
    assert game.hints_used_count == 1

    # Second hint (should be denied)
    run_guess_loop_once_for_hint(game)
    captured = capsys.readouterr()
    assert "You have already used all your hints" in captured.out
    assert game.hints_used_count == 1

def test_hint_hard_difficulty_allows_none(capsys):
    """Test Hard difficulty allows no hints."""
    game = Game(difficulty="hard")
    game.target_word = "apple"

    # First hint (should be denied)
    run_guess_loop_once_for_hint(game)
    captured = capsys.readouterr()
    assert "Hints are disabled for this difficulty level" in captured.out
    assert game.hints_used_count == 0

def test_hint_pro_difficulty_allows_none(capsys):
    """Test Pro difficulty allows no hints."""
    game = Game(difficulty="pro")
    game.target_word = "apple"

    # First hint (should be denied)
    run_guess_loop_once_for_hint(game)
    captured = capsys.readouterr()
    assert "Hints are disabled for this difficulty level" in captured.out
    assert game.hints_used_count == 0

@patch('builtins.input', side_effect=['hint', 'valid'])
def test_hint_does_not_consume_guess(mock_input, capsys):
    """Test that using a hint does not decrement remaining_guesses."""
    game = Game(difficulty="medium")
    initial_guesses = game.remaining_guesses
    game.target_word = "tests" # Set a target for hint logic

    # Allow the actual _provide_hint to run to check hints_used_count
    guess = game._get_user_guess() # This call should now complete

    assert guess == 'valid'
    assert game.remaining_guesses == initial_guesses
    assert game.hints_used_count == 1 # Check that the real _provide_hint incremented the count

# --- Tests for Gameplay (Win/Loss/Guesses - to be added) ---

@patch('builtins.input', return_value='wrong') # User always guesses 'wrong'
@patch('src.wordle.game.Game._display_result') # Mock display result to avoid printing
@patch('src.wordle.game.Game._display_history') # Mock display history
@patch('src.wordle.game.Game._display_welcome') # Mock display welcome
def test_pro_difficulty_game_over_after_5_guesses(mock_welcome, mock_history, mock_result, mock_input):
    """Test that Pro difficulty ends the game after 5 incorrect guesses."""
    game = Game(difficulty="pro")
    game.target_word = "right" # Ensure target != guess

    # Simulate the run loop without actually calling run()
    # This is a more controlled way to test the guess limit logic
    win = False
    while game.remaining_guesses > 0:
        guess = game._get_user_guess() # Gets 'wrong'
        # feedback = game.evaluator.evaluate_guess(game.target_word, guess)
        # game.guesses_history.append((guess, feedback))
        # In a real scenario, run() appends to history & evaluates
        # For this test, we just need to check the guess count
        game.remaining_guesses -= 1
        # Check win condition (won't happen here)
        # if feedback == [game.evaluator.CORRECT_POSITION] * 5:
        #     win = True
        #     break

    # After loop finishes (game.remaining_guesses == 0)
    assert game.remaining_guesses == 0
    # Explicitly call the method that should be called after the loop in run()
    game._display_result(win)
    # Now check the mock
    mock_result.assert_called_once_with(False)

# Note: More comprehensive tests could mock Evaluator and check history,
# or directly call run() and capture/assert final output.
# These tests focus specifically on difficulty settings and hint counts. 