# CodSoft Task #2: Rock-Paper-Scissors (Simple & Minimalist UI) 🪨📄✂️

A clean, modern, and simple Python implementation of the classic Rock-Paper-Scissors game featuring a **Minimalist Graphical User Interface (GUI)** and a **Command Line Interface (CLI)**.

---

## 🎨 Simple & Minimalist UI Features

* **Clean Layout**: Crisp slate background with un-cluttered typography.
* **Simple Scoreboard**: Displays Player Wins (`YOU`), `TIES`, and `COMPUTER` scores.
* **Clear Action Buttons**: Large, clear buttons for **Rock 🪨**, **Paper 📄**, and **Scissors ✂️**.
* **Visual Result Banner**: Highlights round outcomes (Win, Loss, Tie) with clear explanation text.
* **Reset Scores & Audio Controls**: Simple reset option and subtle sound effects toggle.

---

## 📋 Task Requirements Met

| Requirement | Implementation Details |
| :--- | :--- |
| **User Input** | Clear move buttons (🪨 Rock, 📄 Paper, ✂️ Scissors) in GUI mode, or single-key/name prompt in CLI mode. |
| **Computer Selection** | Random choice generation for CPU with clean selection animation. |
| **Game Logic** | Rules enforced: Rock beats Scissors, Scissors beats Paper, Paper beats Rock. |
| **Display Result** | Shows both player's and computer's choices, announces winner/tie in clear color-coded banners. |
| **Score Tracking** | Scoreboard tracking Player Wins, Computer Wins, and Ties. |
| **Play Again** | Continuous round play with a dedicated "Reset Scores" button. |
| **User Interface** | Simple, clean, minimalist GUI design focused on ease of use. |

---

## 📁 File Structure

```
codsoft_taskno2_rock-paper-scissor-game/
├── main.py           # Main entry point (launches GUI default, supports --cli)
├── gui_app.py        # Simple & Minimalist GUI application
├── cli_app.py        # Terminal Command Line Interface app
├── game_logic.py     # Core game rules, winner calculation, & ScoreTracker
├── test_game.py      # Automated unit tests for game logic & score tracking
└── README.md         # Documentation & execution guide
```

---

## 🚀 How to Run

### 1. Launch Simple GUI (Default)
```bash
python main.py
```

### 2. Launch CLI Mode (Terminal Interface)
```bash
python main.py --cli
```

### 3. Run Automated Unit Tests
```bash
python test_game.py
```

Expected Output:
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

---

## ⚙️ Requirements & Dependencies
* **Python**: 3.7 or higher.
* **Dependencies**: Uses standard Python libraries (`tkinter`, `winsound`, `threading`, `random`, `unittest`, `argparse`). Zero `pip install` required!
