"""
main.py - Entry point for the Rock-Paper-Scissors application.
Supports launching either the Graphical User Interface (GUI) or Command Line Interface (CLI).
"""

import sys
import argparse
import tkinter as tk

from gui_app import launch_gui
from cli_app import run_cli_game


def main():
    parser = argparse.ArgumentParser(description="CodSoft Task 2: Rock-Paper-Scissors Game")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run the game in Command Line Interface (CLI) mode"
    )
    args = parser.parse_args()

    if args.cli:
        print("Starting Rock-Paper-Scissors in CLI mode...\n")
        run_cli_game()
    else:
        try:
            print("Launching Rock-Paper-Scissors GUI application...")
            launch_gui()
        except tk.TclError as e:
            print(f"⚠️ Could not launch GUI environment ({e}). Falling back to CLI mode...\n")
            run_cli_game()


if __name__ == "__main__":
    main()
