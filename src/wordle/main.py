import argparse # Added for command-line arguments
from .game import Game

def main():
    """Sets up the game with command-line argument parsing and runs it."""
    parser = argparse.ArgumentParser(description="Play a game of Wordle in the terminal.")
    parser.add_argument(
        "-l", "--level",
        type=str,
        choices=["easy", "medium", "hard", "pro"],
        default="medium",
        help="Set the game difficulty level (default: medium)",
        metavar="LEVEL"
    )
    args = parser.parse_args()

    # Convert level to lowercase for consistent handling in Game class
    difficulty = args.level.lower()

    print(f"Starting Wordle game (Difficulty: {difficulty.capitalize()})")
    game = Game(difficulty=difficulty) # Pass difficulty to Game constructor
    game.run()

if __name__ == "__main__":
    main() 