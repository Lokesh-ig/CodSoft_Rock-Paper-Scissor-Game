"""
test_game.py - Unit tests for Rock-Paper-Scissors game logic.
"""

import unittest
from game_logic import (
    determine_winner,
    get_computer_choice,
    ScoreTracker,
    CHOICES
)


class TestRockPaperScissorsLogic(unittest.TestCase):

    def test_computer_choice_valid(self):
        for _ in range(50):
            choice = get_computer_choice()
            self.assertIn(choice, CHOICES)

    def test_determine_winner_outcomes(self):
        # User Wins
        res, msg = determine_winner("rock", "scissors")
        self.assertEqual(res, "win")
        self.assertIn("Rock smashes Scissors", msg)

        res, msg = determine_winner("scissors", "paper")
        self.assertEqual(res, "win")
        self.assertIn("Scissors cuts Paper", msg)

        res, msg = determine_winner("paper", "rock")
        self.assertEqual(res, "win")
        self.assertIn("Paper covers Rock", msg)

        # Computer Wins (User Loses)
        res, msg = determine_winner("scissors", "rock")
        self.assertEqual(res, "lose")

        res, msg = determine_winner("paper", "scissors")
        self.assertEqual(res, "lose")

        res, msg = determine_winner("rock", "paper")
        self.assertEqual(res, "lose")

        # Ties
        for choice in CHOICES:
            res, msg = determine_winner(choice, choice)
            self.assertEqual(res, "tie")
            self.assertIn("tie", msg)

    def test_invalid_choices(self):
        with self.assertRaises(ValueError):
            determine_winner("fire", "rock")
        with self.assertRaises(ValueError):
            determine_winner("rock", "water")

    def test_score_tracker_streaks_and_stats(self):
        tracker = ScoreTracker(target_wins=2)
        self.assertEqual(tracker.user_score, 0)
        self.assertEqual(tracker.current_streak, 0)

        # Round 1: Win
        res, exp = determine_winner("rock", "scissors")
        tracker.record_round("rock", "scissors", res, exp)
        self.assertEqual(tracker.user_score, 1)
        self.assertEqual(tracker.current_streak, 1)
        self.assertEqual(tracker.win_rate, 100.0)

        # Round 2: Win -> Reaches target_wins = 2
        res, exp = determine_winner("rock", "scissors")
        tracker.record_round("rock", "scissors", res, exp)
        self.assertEqual(tracker.user_score, 2)
        self.assertEqual(tracker.current_streak, 2)

        match_over, winner = tracker.is_match_over()
        self.assertTrue(match_over)
        self.assertEqual(winner, "Player")

        # Check Achievements
        self.assertIn("First Victory 🏆", tracker.achievements)

        # Reset
        tracker.reset()
        self.assertEqual(tracker.user_score, 0)
        self.assertEqual(tracker.current_streak, 0)
        self.assertEqual(len(tracker.history), 0)


if __name__ == "__main__":
    unittest.main()
