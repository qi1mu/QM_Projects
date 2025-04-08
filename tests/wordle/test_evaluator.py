import pytest
from src.wordle.evaluator import Evaluator

@pytest.fixture
def evaluator():
    """Provides an instance of the Evaluator class."""
    return Evaluator()

# Parameterized test cases for evaluate_guess
# Format: (target_word, guess, expected_feedback_list)
evaluate_test_cases = [
    # Basic Cases
    ("apple", "apple", ["*", "*", "*", "*", "*"]), # Perfect match
    ("tests", "tests", ["*", "*", "*", "*", "*"]), # Perfect match 2
    ("crane", "tests", ["_", "+", "_", "_", "_"]), # Corrected: e is present
    ("apple", "plant", ["+", "+", "+", "_", "_"]), # Corrected: p,l,a are present
    ("table", "cable", ["_", "*", "*", "*", "*"]), # Corrected: c != t
    ("audio", "radio", ["_", "+", "*", "*", "*"]), # Corrected: r+, a*, d*, i*, o*

    # Duplicate Letters in Target
    ("apple", "level", ["+", "+", "_", "_", "_"]), # Corrected: l+, e+, v_, e!=l(_), l -> used up
    ("apple", "apply", ["*", "*", "*", "*", "_"]), # Corrected: y is not in apple
    ("apple", "kappa", ["_", "+", "*", "+", "_"]), # Corrected: k_, a+, p*, p+, a_
    ("teeth", "sheet", ["_", "+", "*", "+", "+"]), # Corrected: s_, h+, e*, e+, t+
    ("booth", "tooth", ["_", "*", "*", "*", "*"]), # Corrected: b != t

    # Duplicate Letters in Guess
    ("crane", "eerie", ["_", "_", "+", "_", "*"]), # Corrected: e_, e_, r+, i_, e*
    ("apple", "peppy", ["+", "+", "*", "_", "_"]), # Corrected: p+, e+, p*, p_, y_
    ("chess", "seeks", ["+", "_", "*", "_", "*"]), # Corrected: s+, e!=e, e*, k!=s, s*
    ("array", "radar", ["+", "+", "_", "*", "+"]), # Corrected: r+, a+, d_, a*, r+

    # Edge Cases from Design Doc / Previous Examples
    ("apple", "peeel", ["+", "+", "_", "_", "+"]), # Verified case: P+, E+, E_, E_, L+
    ("flame", "bread", ["_", "_", "+", "+", "_"]), # B_, R_, E+, A+, D_
    ("flame", "flake", ["*", "*", "*", "_", "*"]), # F*, L*, A*, K_, E*

    # Cases from WordManager test block if relevant
    ("apple", "zzzzz", ["_", "_", "_", "_", "_"]),

    # Additional tricky cases
    ("abbey", "babel", ["+", "+", "*", "*", "_"]), # Corrected: b+, a+, b*, e*, l_
    ("sassy", "assay", ["+", "+", "*", "_", "*"]), # Corrected: a+, s+, s*, a_, y*

]

@pytest.mark.parametrize("target, guess, expected", evaluate_test_cases)
def test_evaluate_guess(evaluator, target, guess, expected):
    """Tests the evaluate_guess method with various scenarios."""
    result = evaluator.evaluate_guess(target, guess)
    assert result == expected, f"Failed for Target: {target}, Guess: {guess}. Expected {expected}, Got {result}"

# Test invalid input handling
def test_evaluate_guess_invalid_length(evaluator):
    """Tests that evaluate_guess raises ValueError for incorrect lengths."""
    with pytest.raises(ValueError):
        evaluator.evaluate_guess("apple", "apples") # Guess too long
    with pytest.raises(ValueError):
        evaluator.evaluate_guess("apples", "apple") # Target too long
    with pytest.raises(ValueError):
        evaluator.evaluate_guess("four", "five")    # Both wrong length
    with pytest.raises(ValueError):
        evaluator.evaluate_guess("", "")           # Empty strings 