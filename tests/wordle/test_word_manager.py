import pytest
import os
import tempfile
from src.wordle.word_manager import WordManager

# Helper to create a temporary word file
@pytest.fixture
def temp_word_file():
    words = ["apple", "table", "chair", "crane", "brick"]
    # Use NamedTemporaryFile to handle cleanup automatically
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as tmp_file:
        tmp_file.write("\n".join(words))
        file_path = tmp_file.name
    yield file_path
    os.remove(file_path) # Ensure removal after test yields

@pytest.fixture
def temp_word_file_mixed():
    words = ["apple", "table", "chair", "crane", "brick", "banana", "tst", "12345", " "]
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as tmp_file:
        tmp_file.write("\n".join(words))
        file_path = tmp_file.name
    yield file_path
    os.remove(file_path)

@pytest.fixture
def empty_temp_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as tmp_file:
        file_path = tmp_file.name
    yield file_path
    os.remove(file_path)


# Test WordManager Initialization and Loading
def test_word_manager_loads_correctly(temp_word_file):
    """Tests if WordManager loads the correct words from a temp file."""
    # We need to override the default path finding logic for the test
    # Assuming the test runs from the project root, we can pass the temp path directly
    # The original __init__ constructs path based on __file__, which won't work here easily.
    # Alternative: Mock os.path functions or refactor WordManager to accept absolute path directly.

    # Let's refactor WordManager slightly for testability (or mock)
    # For simplicity here, we assume WordManager can accept a full path
    # or we adjust the test environment setup.

    # Mocking approach (if WordManager wasn't easily adaptable):
    # with patch('src.wordle.word_manager.os.path.abspath') as mock_abspath,
    #      patch('src.wordle.word_manager.os.path.dirname') as mock_dirname,
    #      patch('src.wordle.word_manager.os.path.join') as mock_join:
    #     mock_join.return_value = temp_word_file # Force it to use the temp file
    #     manager = WordManager() # Now __init__ will use the mocked path

    # Simpler Approach: Modify WordManager to accept full path or test differently
    # Let's assume we test the _load_words method directly or pass full path

    # Test _load_words directly for simplicity in this example
    manager = WordManager.__new__(WordManager) # Create instance without calling __init__
    loaded_words = manager._load_words(temp_word_file)

    assert len(loaded_words) == 5
    assert "apple" in loaded_words
    assert "table" in loaded_words
    assert "chair" in loaded_words
    assert "crane" in loaded_words
    assert "brick" in loaded_words

def test_word_manager_filters_words(temp_word_file_mixed):
    """Tests if WordManager filters out non-5-letter and non-alpha words."""
    manager = WordManager.__new__(WordManager)
    loaded_words = manager._load_words(temp_word_file_mixed)

    assert len(loaded_words) == 5 # Only the 5-letter alpha words
    assert "apple" in loaded_words
    assert "table" in loaded_words
    assert "chair" in loaded_words
    assert "crane" in loaded_words
    assert "brick" in loaded_words
    assert "banana" not in loaded_words # 6 letters
    assert "tst" not in loaded_words    # 3 letters
    assert "12345" not in loaded_words  # Non-alpha

def test_word_manager_handles_file_not_found():
    """Tests WordManager handling when the word file does not exist."""
    manager = WordManager.__new__(WordManager)
    # Capture print output or check for specific return value/exception
    loaded_words = manager._load_words("non_existent_file.txt")
    assert loaded_words == []
    # We might want to check stderr/stdout for the error message too

def test_word_manager_handles_empty_file(empty_temp_file):
    """Tests WordManager handling for an empty word file."""
    manager = WordManager.__new__(WordManager)
    loaded_words = manager._load_words(empty_temp_file)
    assert loaded_words == []

# Test Word Selection
def test_select_target_word(temp_word_file):
    """Tests if the selected target word is from the loaded list."""
    # Need a fully initialized manager for this
    # Option 1: Use the actual data file (less isolated)
    # Option 2: Adapt __init__ or mock path finding

    # Mocking the internal _load_words result is often cleanest
    class MockWordManager(WordManager):
        def _load_words(self, file_path):
            # Use the fixture data directly, bypass file reading
            return ["apple", "table", "chair", "crane", "brick"]

    manager = MockWordManager.__new__(MockWordManager)
    manager.word_list = manager._load_words(temp_word_file) # Manually set word_list
    manager.target_word = manager._select_target_word()

    assert manager.target_word in ["apple", "table", "chair", "crane", "brick"]

# Test Word Validation
@pytest.fixture
def manager_with_temp_list(temp_word_file):
    """Provides a WordManager instance initialized with the temp word list."""
    # Using the Mock approach for clean initialization
    class MockWordManager(WordManager):
        def _load_words(self, file_path):
             return ["apple", "table", "chair", "crane", "brick"]

    manager = MockWordManager.__new__(MockWordManager)
    manager.word_list = manager._load_words(temp_word_file)
    # No need to select target word for validation tests
    return manager

def test_is_valid_word_positive(manager_with_temp_list):
    """Tests is_valid_word for words present in the list."""
    assert manager_with_temp_list.is_valid_word("apple") == True
    assert manager_with_temp_list.is_valid_word("TABLE") == True # Case-insensitive
    assert manager_with_temp_list.is_valid_word("brick") == True

def test_is_valid_word_negative(manager_with_temp_list):
    """Tests is_valid_word for words not present in the list."""
    assert manager_with_temp_list.is_valid_word("grape") == False
    assert manager_with_temp_list.is_valid_word("apples") == False # Wrong length
    assert manager_with_temp_list.is_valid_word("") == False
    assert manager_with_temp_list.is_valid_word("12345") == False 