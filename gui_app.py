"""
gui_app.py - Stylish, Clean & Reliable Rock-Paper-Scissors Application.
Instant move evaluation, hover effects, score tracking, 1P/2P modes,
Light/Dark themes, and match history log table.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import Dict, Any, Optional

from game_logic import determine_winner, get_computer_choice, ScoreTracker, CHOICES, CHOICE_EMOJIS, CHOICE_NAMES

# Stylish Light & Dark Theme Palette Definitions
THEME_LIGHT = {
    "name": "light",
    "bg": "#f8fafc",
    "card": "#ffffff",
    "border": "#cbd5e1",
    "text": "#0f172a",
    "muted": "#64748b",
    "accent": "#3b82f6",
    "accent_hover": "#1d4ed8",
    "win": "#10b981",
    "lose": "#f43f5e",
    "tie": "#0284c7",
    "banner_bg": "#e2e8f0",
    "tree_bg": "#ffffff",
    "tree_fg": "#0f172a",
    "tree_head_bg": "#e2e8f0",
    "btn_bg": "#3b82f6",
    "btn_hover": "#2563eb",
    "btn_fg": "#ffffff",
    "reset_bg": "#ffffff",
    "reset_hover": "#e2e8f0"
}

THEME_DARK = {
    "name": "dark",
    "bg": "#0f172a",
    "card": "#1e293b",
    "border": "#334155",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "accent": "#6366f1",
    "accent_hover": "#4338ca",
    "win": "#34d399",
    "lose": "#fb7185",
    "tie": "#60a5fa",
    "banner_bg": "#1e293b",
    "tree_bg": "#1e293b",
    "tree_fg": "#f8fafc",
    "tree_head_bg": "#334155",
    "btn_bg": "#6366f1",
    "btn_hover": "#4f46e5",
    "btn_fg": "#ffffff",
    "reset_bg": "#1e293b",
    "reset_hover": "#334155"
}


def add_hover_effect(widget: tk.Widget, normal_bg: str, hover_bg: str):
    """Add mouse cursor hover effects to a Tkinter widget."""
    widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg) if widget.cget("state") != "disabled" else None)
    widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg) if widget.cget("state") != "disabled" else None)


class CompleteRPSGUI:
    """Stylish & Reliable Interface for Rock-Paper-Scissors."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Rock Paper Scissors Championship")
        self.root.geometry("640x740")
        self.root.minsize(540, 660)

        self.current_theme = THEME_LIGHT
        self.root.configure(bg=self.current_theme["bg"])

        self.tracker = ScoreTracker()

        # 2 Player Mode State
        self.is_two_player: bool = False
        self.p1_choice: Optional[str] = None
        self.current_turn: int = 1  # 1 for P1, 2 for P2

        self._configure_styles()
        self._build_ui()
        self._apply_theme()

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def _build_ui(self):
        """Construct main responsive UI layout."""
        # Top Header Bar
        self.top_bar = tk.Frame(self.root, pady=10, padx=18)
        self.top_bar.pack(fill="x", side="top")

        # Mode Selector Buttons
        self.mode_var = tk.StringVar(value="1P")
        
        mode_box = tk.Frame(self.top_bar)
        mode_box.pack(side="left")

        self.mode_1p_rb = tk.Radiobutton(
            mode_box,
            text="👤 1 Player",
            value="1P",
            variable=self.mode_var,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            command=self._on_mode_change
        )
        self.mode_1p_rb.pack(side="left", padx=4)

        self.mode_2p_rb = tk.Radiobutton(
            mode_box,
            text="👥 2 Players",
            value="2P",
            variable=self.mode_var,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            command=self._on_mode_change
        )
        self.mode_2p_rb.pack(side="left", padx=4)

        # Light/Dark Theme Toggle Button
        self.theme_btn = tk.Button(
            self.top_bar,
            text="🌙 Dark Mode",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="right", padx=4)

        # Main Container
        self.main_container = tk.Frame(self.root, padx=22, pady=8)
        self.main_container.pack(fill="both", expand=True)

        # 1. Header Title
        self.title_lbl = tk.Label(
            self.main_container,
            text="Rock • Paper • Scissors",
            font=("Segoe UI", 20, "bold")
        )
        self.title_lbl.pack(pady=(0, 2))

        self.sub_lbl = tk.Label(
            self.main_container,
            text="Single Player vs Computer Mode",
            font=("Segoe UI", 9)
        )
        self.sub_lbl.pack(pady=(0, 10))

        # 2. Stylish Scoreboard Dashboard Card
        self.score_card = tk.Frame(
            self.main_container,
            highlightthickness=1,
            padx=12,
            pady=10
        )
        self.score_card.pack(fill="x", pady=(0, 10))

        self.score_card.columnconfigure(0, weight=1)
        self.score_card.columnconfigure(1, weight=1)
        self.score_card.columnconfigure(2, weight=1)

        # Player 1 Score Box
        u_box = tk.Frame(self.score_card, padx=10, pady=4)
        u_box.grid(row=0, column=0)
        self.lbl_p1_name = tk.Label(u_box, text="PLAYER 1", font=("Segoe UI", 9, "bold"))
        self.lbl_p1_name.pack()
        self.p1_score_lbl = tk.Label(u_box, text="0", font=("Segoe UI", 26, "bold"))
        self.p1_score_lbl.pack()

        # Ties Box
        t_box = tk.Frame(self.score_card, padx=10, pady=4)
        t_box.grid(row=0, column=1)
        self.lbl_t_title = tk.Label(t_box, text="TIES", font=("Segoe UI", 9, "bold"))
        self.lbl_t_title.pack()
        self.t_score_lbl = tk.Label(t_box, text="0", font=("Segoe UI", 26, "bold"))
        self.t_score_lbl.pack()

        # Player 2 / CPU Score Box
        c_box = tk.Frame(self.score_card, padx=10, pady=4)
        c_box.grid(row=0, column=2)
        self.lbl_p2_name = tk.Label(c_box, text="CPU", font=("Segoe UI", 9, "bold"))
        self.lbl_p2_name.pack()
        self.p2_score_lbl = tk.Label(c_box, text="0", font=("Segoe UI", 26, "bold"))
        self.p2_score_lbl.pack()

        # 3. Move Display Cards Frame
        self.arena_frame = tk.Frame(self.main_container)
        self.arena_frame.pack(fill="x", pady=6)
        self.arena_frame.columnconfigure(0, weight=1)
        self.arena_frame.columnconfigure(1, weight=0)
        self.arena_frame.columnconfigure(2, weight=1)

        self.user_card = tk.Label(
            self.arena_frame,
            text="❓\nPlayer 1",
            font=("Segoe UI", 16),
            width=10,
            height=3,
            relief="solid",
            bd=1
        )
        self.user_card.grid(row=0, column=0, sticky="ew", padx=6)

        self.vs_lbl = tk.Label(self.arena_frame, text="VS", font=("Segoe UI", 14, "bold"))
        self.vs_lbl.grid(row=0, column=1, padx=12)

        self.comp_card = tk.Label(
            self.arena_frame,
            text="❓\nCPU Move",
            font=("Segoe UI", 16),
            width=10,
            height=3,
            relief="solid",
            bd=1
        )
        self.comp_card.grid(row=0, column=2, sticky="ew", padx=6)

        # 4. Turn & Result Banner
        self.result_banner = tk.Label(
            self.main_container,
            text="Select your move to play!",
            font=("Segoe UI", 11, "bold"),
            pady=10,
            padx=12,
            wraplength=540
        )
        self.result_banner.pack(fill="x", pady=10)

        # 5. Action Move Buttons Frame
        self.btn_frame = tk.Frame(self.main_container)
        self.btn_frame.pack(fill="x", pady=6)
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)

        moves = [("Rock 🪨", "rock"), ("Paper 📄", "paper"), ("Scissors ✂️", "scissors")]
        self.move_buttons = []

        for idx, (label_text, move_key) in enumerate(moves):
            btn = tk.Button(
                self.btn_frame,
                text=label_text,
                font=("Segoe UI", 11, "bold"),
                relief="flat",
                bd=0,
                pady=12,
                cursor="hand2",
                command=lambda m=move_key: self._on_move_click(m)
            )
            btn.grid(row=0, column=idx, padx=5, sticky="ew")
            self.move_buttons.append(btn)

        # 6. Round History Log Table
        self.hist_lbl = tk.Label(
            self.main_container,
            text="📜 Match History Log",
            font=("Segoe UI", 10, "bold")
        )
        self.hist_lbl.pack(anchor="w", pady=(10, 4))

        self.table_frame = tk.Frame(self.main_container)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("round", "p1", "p2", "result", "explanation")
        self.history_tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=4)

        self.history_tree.heading("round", text="Rd #")
        self.history_tree.heading("p1", text="Player 1")
        self.history_tree.heading("p2", text="P2 / CPU")
        self.history_tree.heading("result", text="Outcome")
        self.history_tree.heading("explanation", text="Details")

        self.history_tree.column("round", width=50, anchor="center")
        self.history_tree.column("p1", width=95, anchor="center")
        self.history_tree.column("p2", width=95, anchor="center")
        self.history_tree.column("result", width=85, anchor="center")
        self.history_tree.column("explanation", width=230, anchor="w")

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 7. Bottom Controls Bar
        self.bottom_frame = tk.Frame(self.root, pady=10)
        self.bottom_frame.pack(fill="x", side="bottom")

        self.reset_btn = tk.Button(
            self.bottom_frame,
            text="🔄 Reset Scores & History",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=14,
            pady=5,
            cursor="hand2",
            command=self._confirm_reset
        )
        self.reset_btn.pack(side="left", padx=22)

    def _toggle_theme(self):
        """Toggle between Light Mode and Dark Mode."""
        if self.current_theme["name"] == "light":
            self.current_theme = THEME_DARK
            self.theme_btn.config(text="☀️ Light Mode")
        else:
            self.current_theme = THEME_LIGHT
            self.theme_btn.config(text="🌙 Dark Mode")

        self._apply_theme()

    def _apply_theme(self):
        """Apply active theme colors and hover effects to all elements."""
        t = self.current_theme
        self.root.configure(bg=t["bg"])
        self.top_bar.configure(bg=t["bg"])
        self.main_container.configure(bg=t["bg"])
        self.score_card.configure(bg=t["card"], highlightbackground=t["border"])
        self.arena_frame.configure(bg=t["bg"])
        self.btn_frame.configure(bg=t["bg"])
        self.table_frame.configure(bg=t["bg"])
        self.bottom_frame.configure(bg=t["bg"])

        for rb in (self.mode_1p_rb, self.mode_2p_rb):
            rb.configure(bg=t["bg"], fg=t["text"], activebackground=t["bg"], selectcolor=t["bg"])

        self.theme_btn.configure(bg=t["card"], fg=t["accent"], activebackground=t["border"])
        add_hover_effect(self.theme_btn, t["card"], t["border"])

        self.title_lbl.configure(bg=t["bg"], fg=t["text"])
        self.sub_lbl.configure(bg=t["bg"], fg=t["muted"])

        for box in self.score_card.winfo_children():
            box.configure(bg=t["card"])
            for child in box.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=t["card"])

        self.lbl_p1_name.configure(fg=t["win"])
        self.lbl_t_title.configure(fg=t["tie"])
        self.lbl_p2_name.configure(fg=t["lose"])

        self.p1_score_lbl.configure(fg=t["text"])
        self.t_score_lbl.configure(fg=t["text"])
        self.p2_score_lbl.configure(fg=t["text"])

        self.user_card.configure(bg=t["card"], fg=t["text"], highlightbackground=t["border"])
        self.vs_lbl.configure(bg=t["bg"], fg=t["muted"])
        self.comp_card.configure(bg=t["card"], fg=t["text"], highlightbackground=t["border"])

        self.result_banner.configure(bg=t["banner_bg"], fg=t["text"])
        self.hist_lbl.configure(bg=t["bg"], fg=t["muted"])

        # Apply Move Button Theme & Hover Effects
        for btn in self.move_buttons:
            btn.configure(bg=t["btn_bg"], fg=t["btn_fg"], activebackground=t["btn_hover"])
            add_hover_effect(btn, t["btn_bg"], t["btn_hover"])

        self.style.configure(
            "Treeview",
            background=t["tree_bg"],
            foreground=t["tree_fg"],
            fieldbackground=t["tree_bg"],
            rowheight=25,
            font=("Segoe UI", 9)
        )
        self.style.configure(
            "Treeview.Heading",
            background=t["tree_head_bg"],
            foreground=t["tree_fg"],
            font=("Segoe UI", 9, "bold")
        )

        self.reset_btn.configure(bg=t["reset_bg"], fg=t["text"], activebackground=t["reset_hover"])
        add_hover_effect(self.reset_btn, t["reset_bg"], t["reset_hover"])

    def _on_mode_change(self):
        """Switch between 1 Player and 2 Player Mode."""
        mode = self.mode_var.get()
        self.is_two_player = (mode == "2P")
        self.p1_choice = None
        self.current_turn = 1

        if self.is_two_player:
            self.sub_lbl.config(text="Two Player Pass-and-Play Mode")
            self.lbl_p2_name.config(text="PLAYER 2")
            self.comp_card.config(text="❓\nPlayer 2")
            self.result_banner.config(text="Player 1: Select your move below!")
        else:
            self.sub_lbl.config(text="Single Player vs Computer Mode")
            self.lbl_p2_name.config(text="CPU")
            self.comp_card.config(text="❓\nCPU Move")
            self.result_banner.config(text="Select your move to play against CPU!")

        self._confirm_reset(prompt=False)

    def _on_move_click(self, choice: str):
        """Handle move selection for 1P or 2P modes with instant evaluation."""
        if not self.is_two_player:
            # 1 Player vs CPU: Instant Evaluation & Output Guarantee
            u_emoji = CHOICE_EMOJIS[choice]
            u_name = CHOICE_NAMES[choice]
            self.user_card.config(text=f"{u_emoji}\n{u_name}", fg=self.current_theme["win"])

            final_cpu_choice = get_computer_choice()
            c_emoji = CHOICE_EMOJIS[final_cpu_choice]
            c_name = CHOICE_NAMES[final_cpu_choice]
            self.comp_card.config(text=f"{c_emoji}\n{c_name}", fg=self.current_theme["lose"])

            self._finalize_round(choice, final_cpu_choice)
        else:
            # 2 Players Mode (Pass-and-Play)
            if self.current_turn == 1:
                self.p1_choice = choice
                self.current_turn = 2
                self.user_card.config(text="🔒\nMove Locked", fg=self.current_theme["accent"])
                self.result_banner.config(
                    text="Player 1 move locked! Player 2: Select your move below.",
                    bg=self.current_theme["accent"],
                    fg="#ffffff"
                )
            else:
                p2_choice = choice
                p1_choice = self.p1_choice
                self._evaluate_two_player_round(p1_choice, p2_choice)
                self.current_turn = 1
                self.p1_choice = None

    def _evaluate_two_player_round(self, p1_choice: str, p2_choice: str):
        """Evaluate outcome between Player 1 and Player 2."""
        u1_emoji = CHOICE_EMOJIS[p1_choice]
        u1_name = CHOICE_NAMES[p1_choice]
        u2_emoji = CHOICE_EMOJIS[p2_choice]
        u2_name = CHOICE_NAMES[p2_choice]

        self.user_card.config(text=f"{u1_emoji}\n{u1_name}", fg=self.current_theme["win"])
        self.comp_card.config(text=f"{u2_emoji}\n{u2_name}", fg=self.current_theme["lose"])

        result, explanation = determine_winner(p1_choice, p2_choice)
        round_data = self.tracker.record_round(p1_choice, p2_choice, result, explanation)

        # Update Scores
        self.p1_score_lbl.config(text=str(self.tracker.user_score))
        self.p2_score_lbl.config(text=str(self.tracker.computer_score))
        self.t_score_lbl.config(text=str(self.tracker.ties))

        if result == "win":
            self.result_banner.config(
                text=f"🎉 PLAYER 1 WINS ROUND {self.tracker.total_rounds}! • {explanation}",
                bg=self.current_theme["win"],
                fg="#ffffff"
            )
        elif result == "lose":
            self.result_banner.config(
                text=f"🎉 PLAYER 2 WINS ROUND {self.tracker.total_rounds}! • {explanation}",
                bg=self.current_theme["lose"],
                fg="#ffffff"
            )
        else:
            self.result_banner.config(
                text=f"🤝 IT'S A TIE! • {explanation}",
                bg=self.current_theme["tie"],
                fg="#ffffff"
            )

        # Add to History Log
        self.history_tree.insert(
            "",
            0,
            values=(
                round_data["round"],
                f"{round_data['user_choice']} {u1_emoji}",
                f"{round_data['computer_choice']} {u2_emoji}",
                "P1 WIN" if result == "win" else ("P2 WIN" if result == "lose" else "TIE"),
                explanation
            )
        )

    def _finalize_round(self, user_choice: str, computer_choice: str):
        """Evaluate outcome for Single Player mode."""
        result, explanation = determine_winner(user_choice, computer_choice)
        round_data = self.tracker.record_round(user_choice, computer_choice, result, explanation)

        self.p1_score_lbl.config(text=str(self.tracker.user_score))
        self.p2_score_lbl.config(text=str(self.tracker.computer_score))
        self.t_score_lbl.config(text=str(self.tracker.ties))

        if result == "win":
            self.result_banner.config(
                text=f"🎉 YOU WIN ROUND {self.tracker.total_rounds}! • {explanation}",
                bg=self.current_theme["win"],
                fg="#ffffff"
            )
        elif result == "lose":
            self.result_banner.config(
                text=f"💥 CPU WINS ROUND {self.tracker.total_rounds}! • {explanation}",
                bg=self.current_theme["lose"],
                fg="#ffffff"
            )
        else:
            self.result_banner.config(
                text=f"🤝 IT'S A TIE! • {explanation}",
                bg=self.current_theme["tie"],
                fg="#ffffff"
            )

        # Add to History Log
        self.history_tree.insert(
            "",
            0,
            values=(
                round_data["round"],
                f"{round_data['user_choice']} {CHOICE_EMOJIS[user_choice]}",
                f"{round_data['computer_choice']} {CHOICE_EMOJIS[computer_choice]}",
                round_data["result"],
                explanation
            )
        )

    def _confirm_reset(self, prompt: bool = True):
        """Reset scores, history, and UI state."""
        if prompt:
            if not messagebox.askyesno("Reset Scores", "Reset all scores and match history?"):
                return

        self.tracker.reset()
        self.p1_choice = None
        self.current_turn = 1

        self.p1_score_lbl.config(text="0")
        self.p2_score_lbl.config(text="0")
        self.t_score_lbl.config(text="0")

        p2_name = "Player 2" if self.is_two_player else "CPU Move"
        self.user_card.config(text="❓\nPlayer 1", fg=self.current_theme["text"])
        self.comp_card.config(text=f"❓\n{p2_name}", fg=self.current_theme["text"])

        msg = "Player 1: Select your move below!" if self.is_two_player else "Select your move to play against CPU!"
        self.result_banner.config(
            text=msg,
            bg=self.current_theme["banner_bg"],
            fg=self.current_theme["text"]
        )

        for item in self.history_tree.get_children():
            self.history_tree.delete(item)


def launch_gui():
    """Launch Instant & Reliable Responsive GUI."""
    root = tk.Tk()
    app = CompleteRPSGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
