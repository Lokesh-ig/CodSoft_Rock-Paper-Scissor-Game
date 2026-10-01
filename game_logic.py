"""
game_logic.py - Core game engine for Rock-Paper-Scissors.
Provides choice definitions, winner determination, statistics, streak tracking, and achievements.
"""

import random
from typing import Tuple, Dict, List, Optional

CHOICES = ["rock", "paper", "scissors"]

CHOICE_EMOJIS = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️"
}

CHOICE_NAMES = {
    "rock": "Rock",
    "paper": "Paper",
    "scissors": "Scissors"
}

# Define win conditions and descriptions: (winner, loser) -> reason
RULES = {
    ("rock", "scissors"): "Rock smashes Scissors!",
    ("scissors", "paper"): "Scissors cuts Paper!",
    ("paper", "rock"): "Paper covers Rock!"
}


def get_computer_choice() -> str:
    """Randomly select rock, paper, or scissors for the computer."""
    return random.choice(CHOICES)


def determine_winner(user_choice: str, computer_choice: str) -> Tuple[str, str]:
    """
    Determines the outcome of a round.
    
    Returns:
        Tuple[str, str]: (result, explanation)
        - result: 'win', 'lose', or 'tie'
        - explanation: String describing why the result occurred.
    """
    u_choice = user_choice.lower().strip()
    c_choice = computer_choice.lower().strip()

    if u_choice not in CHOICES:
        raise ValueError(f"Invalid choice '{user_choice}'. Must be one of {CHOICES}")
    if c_choice not in CHOICES:
        raise ValueError(f"Invalid choice '{computer_choice}'. Must be one of {CHOICES}")

    if u_choice == c_choice:
        return "tie", f"Both chose {CHOICE_NAMES[u_choice]}. It's a tie!"

    if (u_choice, c_choice) in RULES:
        return "win", RULES[(u_choice, c_choice)]
    else:
        return "lose", RULES[(c_choice, u_choice)]


class ScoreTracker:
    """Tracks game scores, win streaks, move counts, and achievements across rounds."""
    
    def __init__(self, target_wins: int = 0):
        self.target_wins: int = target_wins  # 0 for endless, 2 for Best-of-3, 3 for Best-of-5
        self.user_score: int = 0
        self.computer_score: int = 0
        self.ties: int = 0
        self.total_rounds: int = 0
        self.current_streak: int = 0
        self.best_streak: int = 0
        self.move_counts: Dict[str, int] = {"rock": 0, "paper": 0, "scissors": 0}
        self.achievements: List[str] = []
        self.history: List[Dict[str, str]] = []

    def record_round(self, user_choice: str, computer_choice: str, result: str, explanation: str) -> Dict[str, str]:
        """Record outcome, update streaks, statistics, and unlock achievements."""
        self.total_rounds += 1
        u_key = user_choice.lower()
        if u_key in self.move_counts:
            self.move_counts[u_key] += 1
        
        if result == "win":
            self.user_score += 1
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
        elif result == "lose":
            self.computer_score += 1
            self.current_streak = 0
        elif result == "tie":
            self.ties += 1

        self._check_achievements()

        round_data = {
            "round": self.total_rounds,
            "user_choice": CHOICE_NAMES[u_key],
            "computer_choice": CHOICE_NAMES[computer_choice.lower()],
            "result": result.upper(),
            "explanation": explanation,
            "streak": self.current_streak
        }
        self.history.append(round_data)
        return round_data

    def _check_achievements(self) -> None:
        """Unlock milestone badges."""
        milestones = [
            (self.user_score >= 1, "First Victory 🏆"),
            (self.current_streak >= 3, "Hot Streak (3 Wins) 🔥"),
            (self.current_streak >= 5, "Unstoppable (5 Wins) ⚡"),
            (self.move_counts["rock"] >= 5, "Rock Titan 🪨"),
            (self.move_counts["paper"] >= 5, "Paper Master 📄"),
            (self.move_counts["scissors"] >= 5, "Scissors Ninja ✂️"),
            (self.total_rounds >= 10, "Veteran Player 🎖️")
        ]
        for condition, title in milestones:
            if condition and title not in self.achievements:
                self.achievements.append(title)

    @property
    def win_rate(self) -> float:
        """Calculate player win percentage (excluding ties)."""
        decisive_rounds = self.user_score + self.computer_score
        if decisive_rounds == 0:
            return 0.0
        return (self.user_score / decisive_rounds) * 100.0

    @property
    def favorite_move(self) -> str:
        """Identify player's most used move."""
        max_count = max(self.move_counts.values())
        if max_count == 0:
            return "None"
        for move, count in self.move_counts.items():
            if count == max_count:
                return f"{CHOICE_NAMES[move]} {CHOICE_EMOJIS[move]}"
        return "None"

    def is_match_over(self) -> Tuple[bool, str]:
        """Check if target wins set limit reached in Match Mode."""
        if self.target_wins > 0:
            if self.user_score >= self.target_wins:
                return True, "Player"
            elif self.computer_score >= self.target_wins:
                return True, "Computer"
        return False, ""

    def reset(self, target_wins: Optional[int] = None) -> None:
        """Reset score tracker state."""
        if target_wins is not None:
            self.target_wins = target_wins
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.total_rounds = 0
        self.current_streak = 0
        self.best_streak = 0
        self.move_counts = {"rock": 0, "paper": 0, "scissors": 0}
        self.achievements.clear()
        self.history.clear()

    def get_summary(self) -> str:
        """Return formatted summary of game stats."""
        return (
            f"Rounds: {self.total_rounds} | "
            f"User: {self.user_score} | "
            f"Computer: {self.computer_score} | "
            f"Ties: {self.ties} | "
            f"Win Rate: {self.win_rate:.1f}% | "
            f"Best Streak: {self.best_streak}"
        )
