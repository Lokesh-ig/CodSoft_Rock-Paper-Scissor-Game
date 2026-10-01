"""
cli_app.py - Command Line Interface (CLI) for Rock-Paper-Scissors.
Interactive terminal game with input validation, score tracking, and safe unicode output.
"""

import sys
from game_logic import (
    determine_winner,
    get_computer_choice,
    ScoreTracker,
    CHOICES,
    CHOICE_NAMES
)

# Reconfigure stdout for UTF-8 encoding on Windows consoles if supported
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def safe_print(text: str):
    """Print helper that safely falls back if the console doesn't support full emoji ranges."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Strip non-ASCII characters if terminal doesn't support unicode
        clean_text = text.encode('ascii', errors='ignore').decode('ascii')
        print(clean_text)


def print_banner():
    safe_print("=" * 55)
    safe_print("        [ROCK - PAPER - SCISSORS GAME]        ")
    safe_print("=" * 55)
    safe_print("Rules:")
    safe_print("  * Rock beats Scissors (Rock smashes Scissors)")
    safe_print("  * Scissors beats Paper (Scissors cuts Paper)")
    safe_print("  * Paper beats Rock (Paper covers Rock)")
    safe_print("=" * 55)


def print_scoreboard(tracker: ScoreTracker):
    safe_print("\n" + "-" * 45)
    safe_print(f" SCOREBOARD | Round {tracker.total_rounds}")
    safe_print(f"   You: {tracker.user_score}  |  Computer: {tracker.computer_score}  |  Ties: {tracker.ties}")
    safe_print("-" * 45)


def get_user_choice() -> str:
    """Prompt user for input with shortcuts (1/r/rock, 2/p/paper, 3/s/scissors)."""
    mapping = {
        "1": "rock", "r": "rock", "rock": "rock",
        "2": "paper", "p": "paper", "paper": "paper",
        "3": "scissors", "s": "scissors", "scissors": "scissors"
    }

    while True:
        safe_print("\nChoose your move:")
        safe_print("  [1] Rock (r)")
        safe_print("  [2] Paper (p)")
        safe_print("  [3] Scissors (s)")
        safe_print("  [Q] Quit Game")
        
        try:
            user_input = input("Enter your choice (1-3, name, or Q): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "quit"

        if user_input in ("q", "quit", "exit"):
            return "quit"
        
        if user_input in mapping:
            return mapping[user_input]

        safe_print("Invalid input! Please enter 1, 2, 3, rock, paper, scissors, or Q.")


def run_cli_game():
    """Main CLI game loop."""
    print_banner()
    tracker = ScoreTracker()

    while True:
        user_choice = get_user_choice()
        if user_choice == "quit":
            safe_print("\nExiting game. Thanks for playing!")
            break

        computer_choice = get_computer_choice()
        result, explanation = determine_winner(user_choice, computer_choice)

        tracker.record_round(user_choice, computer_choice, result, explanation)

        u_str = CHOICE_NAMES[user_choice]
        c_str = CHOICE_NAMES[computer_choice]
        
        safe_print("\n" + "-" * 45)
        safe_print(f" Your move:      {u_str}")
        safe_print(f" Computer move:  {c_str}")
        safe_print("-" * 45)

        if result == "win":
            safe_print(f" OUTCOME: YOU WIN! ({explanation})")
        elif result == "lose":
            safe_print(f" OUTCOME: COMPUTER WINS! ({explanation})")
        else:
            safe_print(f" OUTCOME: IT'S A TIE! ({explanation})")

        print_scoreboard(tracker)

        try:
            play_again = input("\nPlay another round? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if play_again not in ("y", "yes"):
            safe_print("\nFinal Game Summary:")
            safe_print(tracker.get_summary())
            safe_print("\nThank you for playing Rock-Paper-Scissors! Bye!")
            break


if __name__ == "__main__":
    run_cli_game()
