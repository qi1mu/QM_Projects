from flask import Flask, render_template, session, redirect, url_for, flash, request
import os
import logging # Added for logging errors

# Import game logic components using relative imports
from .word_manager import WordManager
from .evaluator import Evaluator # Added Evaluator
# from .game_logic import GameState # Keep commented for now

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
# Secret key is needed for session management
# Use a fixed key for development to prevent session loss on reload
# IMPORTANT: Use a secure, environment-variable-based key in production!
app.secret_key = 'dev-secret-only-key' # Replace os.urandom(24)

# --- Define difficulty levels ---
DIFFICULTY_SETTINGS = {
    'easy': {'guesses': 8, 'hints': 2},
    'medium': {'guesses': 6, 'hints': 1},
    'hard': {'guesses': 6, 'hints': 0},
    'pro': {'guesses': 5, 'hints': 0}
}
# Default difficulty
DEFAULT_DIFFICULTY = 'medium'
# ------------------------------------

# --- Word Manager Initialization ---
word_manager = None
# The path should be relative to the word_manager.py file location
word_list_path = "data/words.txt"
try:
    # Pass the relative path expected by WordManager
    word_manager = WordManager(word_list_path)
    # Or rely on the default: word_manager = WordManager()
    logging.info(f"WordManager loaded successfully with {len(word_manager.get_full_word_list())} words.")
except FileNotFoundError:
    # The WordManager's internal error handling will print details
    logging.error(f"Error initializing WordManager. Check previous logs for file path issues.")
except Exception as e:
    logging.error(f"Error loading WordManager: {e}")
# ------------------------------------

# --- Evaluator Initialization ---
evaluator = Evaluator() # Instantiate the evaluator
# ------------------------------------

@app.route('/')
def index():
    if word_manager is None:
        # If WordManager failed to load, show an error message
        flash("Error: Could not load the word list. Please check server logs.", "error")
        return render_template('index.html', game_state=None, error=True)

    # Check if this is a direct page load (refresh) rather than a redirect
    # For direct page loads (refreshes), always start a new game
    is_refresh = 'from_redirect' not in request.args
    
    if is_refresh:
        # Always create a new game on refresh
        # Get previous difficulty to maintain it across refreshes
        previous_difficulty = session.get('game_state', {}).get('difficulty', DEFAULT_DIFFICULTY)
        difficulty = request.args.get('difficulty', previous_difficulty)
        
        # Start completely fresh game
        if 'game_state' in session:
            session.pop('game_state', None)
        
        # Select new random word
        word_manager.select_target_word()
        target_word = word_manager.get_target_word().upper()
        logging.info(f"Page refreshed - starting new game with target: {target_word}")
            
        # Set up fresh game state with the same difficulty
        if difficulty not in DIFFICULTY_SETTINGS:
            difficulty = DEFAULT_DIFFICULTY
                
        difficulty_config = DIFFICULTY_SETTINGS[difficulty]
        attempts = difficulty_config['guesses']
        allowed_hints = difficulty_config['hints']

        session['game_state'] = {
            'target_word': target_word,
            'guesses': [],
            'feedback': [],
            'attempts_left': attempts,
            'message': 'Enter your first guess!',
            'game_over': False,
            'win': False,
            'difficulty': difficulty,
            'allowed_hints': allowed_hints,
            'hints_used': 0
        }
    elif 'game_state' not in session:
        # If coming from redirect but no game state exists
        logging.info("No game state found after redirect, creating new game")
        try:
            # Rest of the existing "new game" logic
            word_manager.select_target_word()
            target_word = word_manager.get_target_word().upper()
            
            difficulty = request.args.get('difficulty', DEFAULT_DIFFICULTY)
            if difficulty not in DIFFICULTY_SETTINGS:
                difficulty = DEFAULT_DIFFICULTY
                
            difficulty_config = DIFFICULTY_SETTINGS[difficulty]
            attempts = difficulty_config['guesses']
            allowed_hints = difficulty_config['hints']

            session['game_state'] = {
                'target_word': target_word,
                'guesses': [],
                'feedback': [],
                'attempts_left': attempts,
                'message': 'Enter your first guess!',
                'game_over': False,
                'win': False,
                'difficulty': difficulty,
                'allowed_hints': allowed_hints,
                'hints_used': 0
            }
        except Exception as e:
            logging.error(f"Error starting new game: {e}")
            flash("Error starting a new game. Please try refreshing.", "error")
            return render_template('index.html', game_state=None, error=True)
    else:
        # Coming from redirect with existing game state - maintain it
        # Ensure existing game states have all required fields for difficulty and hints
        game_state = session['game_state']
        if 'difficulty' not in game_state:
            game_state['difficulty'] = DEFAULT_DIFFICULTY
            logging.info(f"Adding missing 'difficulty' to existing game state: {DEFAULT_DIFFICULTY}")
            
        if 'allowed_hints' not in game_state:
            # Get hints based on difficulty or default to medium difficulty settings
            difficulty = game_state.get('difficulty', DEFAULT_DIFFICULTY)
            allowed_hints = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY])['hints']
            game_state['allowed_hints'] = allowed_hints
            logging.info(f"Adding missing 'allowed_hints' to existing game state: {allowed_hints}")
            
        if 'hints_used' not in game_state:
            game_state['hints_used'] = 0
            logging.info("Adding missing 'hints_used' to existing game state: 0")
            
        # Always ensure attempts_left matches the difficulty setting for consistency
        difficulty = game_state.get('difficulty', DEFAULT_DIFFICULTY)
        if difficulty in DIFFICULTY_SETTINGS:
            expected_attempts = DIFFICULTY_SETTINGS[difficulty]['guesses']
            current_attempts = game_state.get('attempts_left', 0)
            guesses_made = len(game_state.get('guesses', []))
            
            # Calculate correct attempts_left based on difficulty and guesses made
            correct_attempts_left = expected_attempts - guesses_made
            
            # Adjust only if there's a mismatch
            if current_attempts != correct_attempts_left:
                game_state['attempts_left'] = correct_attempts_left
                logging.info(f"Fixed attempts_left to {correct_attempts_left} based on difficulty {difficulty} and {guesses_made} guesses made")
                
        session['game_state'] = game_state
        session.modified = True

    game_state = session.get('game_state', {})
    # logging.info(f"Rendering index with state: {game_state}") # Debug print - can be noisy
    return render_template('index.html', game_state=game_state, error=False, difficulties=DIFFICULTY_SETTINGS)

@app.route('/guess', methods=['POST'])
def handle_guess():
    if word_manager is None:
        flash("Cannot process guess: Word list not loaded.", "error")
        return redirect(url_for('index', from_redirect=1))

    if 'game_state' not in session:
        flash("No active game found. Starting a new one.", "warning")
        return redirect(url_for('index', from_redirect=1))

    game_state = session['game_state'] # Get mutable copy

    if game_state.get('game_over', False):
        flash("The game is over. Start a new game?", "info") # Add a /new_game route later
        return redirect(url_for('index', from_redirect=1))

    guess = request.form.get('guess', '').upper() # Normalize to uppercase

    # --- Input Validation ---
    valid = True
    if len(guess) != 5:
        game_state['message'] = "Guess must be exactly 5 letters long."
        valid = False
    elif not guess.isalpha():
        game_state['message'] = "Guess must contain only letters."
        valid = False
    # Validate directly against WordManager instead of session
    elif not word_manager.is_valid_word(guess):
        logging.error(f"Word validation failed for '{guess}'")
        game_state['message'] = f'"{guess}" is not a valid word in the dictionary.'
        valid = False

    if not valid:
        session['game_state'] = game_state # Save updated message
        session.modified = True # Mark session as modified
        logging.error(f"Validation failed - session state saved")
        return redirect(url_for('index', from_redirect=1))
    # ------------------------

    # --- Process Valid Guess --- (Ensure evaluator handles uppercase)
    target = game_state['target_word'] # Already uppercase
    feedback_symbols = evaluator.evaluate_guess(target, guess) # Fixed parameter order: target first, then guess

    game_state['guesses'].append(guess)
    game_state['feedback'].append(feedback_symbols)
    game_state['attempts_left'] -= 1

    # --- Check Win/Loss Conditions ---
    if guess == target:
        game_state['win'] = True
        game_state['game_over'] = True
        game_state['message'] = f"Congratulations! You guessed the word '{target}' in {len(game_state['guesses'])} tries!"
    elif game_state['attempts_left'] <= 0:
        game_state['game_over'] = True
        game_state['message'] = f"Game Over! You ran out of guesses. The word was '{target}'."
    else:
        game_state['message'] = "Enter your next guess."
    # -------------------------

    session['game_state'] = game_state # Save the updated state
    session.modified = True # Mark session as modified
    logging.info(f"Guess processed: {guess}, Feedback: {feedback_symbols}, State: {game_state}")

    return redirect(url_for('index', from_redirect=1))

@app.route('/new_game')
def new_game():
    # Get the difficulty parameter if provided
    difficulty = request.args.get('difficulty', DEFAULT_DIFFICULTY)
    if difficulty not in DIFFICULTY_SETTINGS:
        difficulty = DEFAULT_DIFFICULTY
        
    # Clear the old game state from the session
    if 'game_state' in session:
        session.pop('game_state', None)
        # Force WordManager to select a new random word
        word_manager.select_target_word()
        logging.info(f"Starting new game via /new_game route with difficulty: {difficulty}")
    else:
        logging.info(f"/new_game called but no existing game state found. Using difficulty: {difficulty}")

    # Redirect back to the index page with difficulty parameter
    return redirect(url_for('index', difficulty=difficulty, from_redirect=1))

@app.route('/hint')
def get_hint():
    """Provides a hint for the current game if available"""
    if word_manager is None:
        flash("Cannot provide hint: Word list not loaded.", "error")
        return redirect(url_for('index', from_redirect=1))

    if 'game_state' not in session:
        flash("No active game found. Starting a new one.", "warning")
        return redirect(url_for('index', from_redirect=1))

    game_state = session['game_state']

    if game_state.get('game_over', False):
        flash("The game is over. Start a new game to use hints.", "info")
        return redirect(url_for('index', from_redirect=1))

    # Check if hints are allowed for this difficulty
    allowed_hints = game_state.get('allowed_hints', 0)
    if allowed_hints <= 0:
        game_state['message'] = "Hints are disabled for this difficulty level."
        session['game_state'] = game_state
        session.modified = True
        return redirect(url_for('index', from_redirect=1))

    # Check if player has used all available hints
    hints_used = game_state.get('hints_used', 0)
    if hints_used >= allowed_hints:
        game_state['message'] = "You have already used all your hints for this game."
        session['game_state'] = game_state
        session.modified = True
        return redirect(url_for('index', from_redirect=1))

    # Generate a hint - find a letter not yet revealed
    target_word = game_state['target_word'] 
    guesses = game_state.get('guesses', [])
    feedback = game_state.get('feedback', [])
    
    # Find positions that haven't been correctly guessed yet
    unrevealed_positions = []
    for i in range(5):  # Assuming 5-letter words
        position_revealed = False
        # Check if this position has been correctly guessed in any previous guess
        for guess_idx, guess_feedback in enumerate(feedback):
            if i < len(guess_feedback) and guess_feedback[i] == evaluator.CORRECT_POSITION:
                position_revealed = True
                break
        if not position_revealed:
            unrevealed_positions.append(i)
    
    if not unrevealed_positions:
        # All positions have been revealed already, which shouldn't happen
        # but we handle it gracefully
        game_state['message'] = "No new hints available - you've already found all correct positions!"
    else:
        # Choose a random unrevealed position
        import random
        hint_position = random.choice(unrevealed_positions)
        hint_letter = target_word[hint_position]
        
        # Update game state with hint
        game_state['hints_used'] = hints_used + 1
        game_state['message'] = f"Hint: Letter at position {hint_position + 1} is '{hint_letter}'."
    
    session['game_state'] = game_state
    session.modified = True
    return redirect(url_for('index', from_redirect=1))

@app.route('/debug')
def debug_session():
    """Debug endpoint to check session state"""
    output = []
    output.append("Session Debug Info:")
    
    # Check if game_state exists in session
    if 'game_state' in session:
        output.append("Game state exists in session")
        
        # Get the game state
        game_state = session['game_state']
        
        # Check game state keys
        output.append(f"Game state keys: {list(game_state.keys())}")
        
        # Check if valid_words is in game_state
        if 'valid_words' in game_state:
            valid_words = game_state['valid_words']
            output.append(f"Valid words list exists with {len(valid_words)} words")
            output.append(f"Sample words (first 10): {valid_words[:10]}")
            
            # Test a few known valid words
            test_words = ["TABLE", "WHICH", "ABOUT", "WORLD", "MONEY"]
            for word in test_words:
                output.append(f"Is '{word}' in valid_words? {word in valid_words}")
                
            # Check target word
            if 'target_word' in game_state:
                output.append(f"Target word: {game_state['target_word']}")
                output.append(f"Is target word in valid_words? {game_state['target_word'] in valid_words}")
        else:
            output.append("ERROR: valid_words not found in game_state!")
    else:
        output.append("ERROR: No game_state in session!")
    
    # Return debug info
    return "<br>".join(output)

# TODO: Add routes for /hint

if __name__ == '__main__':
    # Debug mode should be False in production
    app.run(debug=True, host='0.0.0.0', port=5001) 