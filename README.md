# CodSoft Task #2: Rock-Paper-Scissors Championship 🪨📄✂️

A modern, responsive Rock-Paper-Scissors game featuring a **Python Desktop GUI**, **CLI Interface**, and a **Live Mobile-Responsive Web Application**.

🌐 **Live Web Demo**: [https://task-intern-project.netlify.app](https://task-intern-project.netlify.app)

---

## 🌟 Key Features

* **🌐 Live Web App**: Deployed on Netlify with mobile-responsive design for any browser or phone.
* **👥 2 Players (P1 vs P2) & 👤 1 Player (vs CPU)**: Play single player against the computer or pass-and-play with a friend (`🔒 Move Locked`).
* **☀️ Light & 🌙 Dark Theme Switcher**: Toggle button to switch color themes instantly.
* **📜 Match History Log Table**: Scrollable table tracking every round outcome and explanation.
* **✨ Button Hover Effects**: Smooth hover highlights on all action buttons.
* **💻 Python Desktop App**: Built-in GUI (`main.py`) & Terminal CLI (`main.py --cli`).

---

## 📋 Task Requirements Met

| Requirement | Implementation Details |
| :--- | :--- |
| **User Input** | Clear move buttons (🪨 Rock, 📄 Paper, ✂️ Scissors) in GUI/Web, or shortcut prompt in CLI. |
| **Computer Selection** | Random choice generation for CPU with selection animations. |
| **Game Logic** | Rules enforced: Rock smashes Scissors, Scissors cuts Paper, Paper covers Rock. |
| **Display Result** | Real-time score update with detailed round winner explanation banner. |
| **Score Tracking** | Scoreboard tracking Player 1, Player 2 / CPU, and Ties. |
| **Play Again** | Continuous round play with a dedicated "Reset Scores & History" button. |
| **User Interface** | Stylish, clean, mobile-responsive interface. |

---

## 📁 File Structure

```
codsoft_taskno2_rock-paper-scissor-game/
├── main.py           # Main entry point (launches GUI default, supports --cli)
├── gui_app.py        # Python Desktop GUI application
├── cli_app.py        # Terminal Command Line Interface app
├── index.html        # Deployable mobile-responsive Web App
├── game_logic.py     # Core game rules, winner calculation, & ScoreTracker
├── test_game.py      # Automated unit tests for game logic & score tracking
└── README.md         # Project documentation
```

---

## 🚀 How to Run Locally

### 1. Launch Desktop GUI (Default)
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
* **Dependencies**: Uses standard Python libraries (`tkinter`, `random`, `unittest`, `argparse`, `sys`). Zero `pip install` required!
