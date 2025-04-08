import random
import os

class WordManager:
    """Manages loading, selecting, and validating words for the Wordle game."""

    def __init__(self, word_file_path="data/words.txt"):
        """Initializes the WordManager, loading words from the specified file.

        Args:
            word_file_path (str): The relative path to the word list file
                                    within the src/wordle directory.
        """
        # Construct the absolute path relative to this file's location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_word_file_path = os.path.join(base_dir, word_file_path)

        self.word_list = self._load_words(absolute_word_file_path)
        if not self.word_list:
            raise ValueError(f"Word list at '{absolute_word_file_path}' is empty or could not be loaded.")
        self.target_word = self._select_target_word()

    def _load_words(self, file_path):
        """Loads words from a file, filtering for 5-letter alphabetic words."""
        words = set()
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    if len(word) == 5 and word.isalpha():
                        words.add(word)
        except FileNotFoundError:
            print(f"Error: Word file not found at {file_path}")
            return []
        except Exception as e:
            print(f"Error loading word file: {e}")
            return []
        return list(words)

    def _select_target_word(self):
        """Selects a random word from the loaded list."""
        if not self.word_list:
            return None # Or raise an error
        return random.choice(self.word_list)

    def get_target_word(self):
        """Returns the selected target word."""
        return self.target_word

    def is_valid_word(self, word):
        """Checks if a given word is in the loaded word list."""
        return word.lower() in self.word_list

    def get_full_word_list(self):
        """Returns the full list of valid words."""
        return self.word_list

# Example Usage (for testing)
if __name__ == '__main__':
    try:
        # Assuming words.txt is in a 'data' subdirectory relative to this script
        manager = WordManager()
        print(f"Loaded {len(manager.get_full_word_list())} words.")
        target = manager.get_target_word()
        print(f"Selected target word: {target}")

        # Test validation
        print(f"Is 'apple' valid? {manager.is_valid_word('apple')}")
        print(f"Is 'zzzzz' valid? {manager.is_valid_word('zzzzz')}")
        print(f"Is 'grape' valid? {manager.is_valid_word('grape')}") # Likely False unless added
        print(f"Is 'query' valid? {manager.is_valid_word('query')}")

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 