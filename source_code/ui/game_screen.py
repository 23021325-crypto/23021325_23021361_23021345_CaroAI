from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
from config import BOARD_SIZE, EMPTY, HUMAN, AI, DEFAULT_DEPTH
from game.board import Board
from ai.agent import CaroAgent
from ai.learning import ExperienceMemory
from ui.end_screen import show_end_message

class GameScreen(tk.Frame):
    def __init__(self, master, player_name: str = "Người chơi", back_callback=None):
        super().__init__(master, bg="#f4f6fb")
        self.master = master
        self.player_name = player_name or "Người chơi"
        self.back_callback = back_callback
        self.board = Board()
        self.memory = ExperienceMemory()
        self.agent = CaroAgent(self.memory)
        self.cell = 58
        self.margin = 30
        self.canvas_size = self.margin * 2 + self.cell * BOARD_SIZE
        self.paused = False
        self.game_over = False
        self.last_move = None
        self.move_history: List[Tuple[int, int, str]] = []
        self.ai_history: List[Tuple[str, Tuple[int, int]]] = []
        self._build_ui()
        self.draw_board()

    def _build_ui(self):
        title = tk.Label(self, text="Caro AI - Minimax / Alpha-Beta", font=("Arial", 20, "bold"), bg="#f4f6fb", fg="#203040")
        title.pack(pady=(12, 6))

        body = tk.Frame(self, bg="#f4f6fb")
        body.pack(fill="both", expand=True, padx=14, pady=8)

        left = tk.Frame(body, bg="#f4f6fb")
        left.pack(side="left", padx=(0, 14))

        self.canvas = tk.Canvas(left, width=self.canvas_size, height=self.canvas_size, bg="#f9df9b", highlightthickness=2, highlightbackground="#293241")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_motion)

        right = tk.Frame(body, bg="#ffffff", bd=1, relief="solid")
        right.pack(side="left", fill="y", padx=(8, 0), ipadx=10, ipady=10)

        tk.Label(right, text=f"Người chơi: {self.player_name}", bg="#ffffff", font=("Arial", 12, "bold")).pack(anchor="w", pady=(4, 10))
        tk.Label(right, text="Thuật toán AI", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w")
        self.algorithm_var = tk.StringVar(value="Alpha-Beta")
        ttk.Combobox(right, textvariable=self.algorithm_var, values=["Alpha-Beta", "Minimax"], state="readonly", width=20).pack(anchor="w", pady=(2, 10))

        tk.Label(right, text="Độ sâu tìm kiếm", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w")
        self.depth_var = tk.IntVar(value=DEFAULT_DEPTH)
        ttk.Spinbox(right, from_=1, to=4, textvariable=self.depth_var, width=7).pack(anchor="w", pady=(2, 10))

        self.learning_var = tk.BooleanVar(value=True)
        tk.Checkbutton(right, text="Dùng bộ nhớ học", variable=self.learning_var, bg="#ffffff").pack(anchor="w", pady=(0, 10))

        tk.Button(right, text="Chơi lại", command=self.restart, width=22, bg="#d8eefe").pack(pady=3)
        tk.Button(right, text="Đi lại", command=self.undo, width=22, bg="#e8f5e9").pack(pady=3)
        self.pause_btn = tk.Button(right, text="Tạm dừng", command=self.toggle_pause, width=22, bg="#fff3cd")
        self.pause_btn.pack(pady=3)
        tk.Button(right, text="Xóa bộ nhớ học", command=self.clear_learning, width=22, bg="#ffe0e0").pack(pady=3)
        if self.back_callback:
            tk.Button(right, text="Về màn hình đầu", command=self.back_callback, width=22).pack(pady=3)

        tk.Label(right, text="Thông tin AI", bg="#ffffff", font=("Arial", 11, "bold")).pack(anchor="w", pady=(14, 4))
        self.info = tk.Text(right, width=42, height=18, wrap="word", font=("Consolas", 9))
        self.info.pack()
        self.log("Bạn là X, máy là O. Bấm vào ô trống để đánh.")
        self.update_learning_label()

    def update_learning_label(self):
        self.log(f"Số ván AI đã học: {self.memory.games_learned}")

    def log(self, msg: str):
        self.info.insert("end", msg + "\n")
        self.info.see("end")

    def draw_board(self):
        self.canvas.delete("all")
        # Grid
        for i in range(BOARD_SIZE + 1):
            x = self.margin + i * self.cell
            y = self.margin + i * self.cell
            self.canvas.create_line(self.margin, y, self.margin + BOARD_SIZE * self.cell, y, fill="#293241")
            self.canvas.create_line(x, self.margin, x, self.margin + BOARD_SIZE * self.cell, fill="#293241")

        # Stones
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board.grid[r][c]
                if piece == EMPTY:
                    continue
                x = self.margin + c * self.cell + self.cell / 2
                y = self.margin + r * self.cell + self.cell / 2
                if self.last_move == (r, c):
                    self.canvas.create_oval(x - 24, y - 24, x + 24, y + 24, outline="#ffb703", width=4)
                if piece == HUMAN:
                    self.canvas.create_line(x - 18, y - 18, x + 18, y + 18, fill="#d62828", width=5)
                    self.canvas.create_line(x + 18, y - 18, x - 18, y + 18, fill="#d62828", width=5)
                else:
                    self.canvas.create_oval(x - 19, y - 19, x + 19, y + 19, outline="#003049", width=5)

    def cell_from_event(self, event):
        col = int((event.x - self.margin) // self.cell)
        row = int((event.y - self.margin) // self.cell)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None

    def on_motion(self, event):
        if self.game_over or self.paused:
            self.canvas.config(cursor="arrow")
            return
        cell = self.cell_from_event(event)
        if cell and self.board.is_empty(*cell):
            self.canvas.config(cursor="hand2")
        else:
            self.canvas.config(cursor="arrow")

    def on_click(self, event):
        if self.game_over or self.paused:
            return
        cell = self.cell_from_event(event)
        if not cell:
            return
        r, c = cell
        if not self.board.make_move(r, c, HUMAN):
            return
        self.move_history.append((r, c, HUMAN))
        self.last_move = (r, c)
        self.draw_board()
        self.log(f"Người chơi đánh: ({r}, {c})")
        if self.check_end():
            return
        self.after(150, self.ai_turn)

    def ai_turn(self):
        if self.game_over or self.paused:
            return
        state_before = self.board.serialize()
        info = self.agent.choose_move(self.board, self.algorithm_var.get(), int(self.depth_var.get()), self.learning_var.get())
        if info.move is None:
            return
        r, c = info.move
        self.board.make_move(r, c, AI)
        self.move_history.append((r, c, AI))
        self.ai_history.append((state_before, (r, c)))
        self.last_move = (r, c)
        self.draw_board()
        self.log(f"AI đánh: ({r}, {c}) | {info.algorithm} depth={info.depth}")
        self.log(f"Điểm={info.score} | Trạng thái xét={info.nodes} | Thời gian={info.elapsed:.4f}s")
        self.log(f"Lý do: {info.reason}")
        self.check_end()

    def check_end(self):
        winner = self.board.check_winner()
        if not winner:
            return False
        self.game_over = True
        if winner == HUMAN:
            result = "HUMAN_WIN"
            title = "Bạn thắng"
            msg = "Chúc mừng! Bạn đã thắng AI."
        elif winner == AI:
            result = "AI_WIN"
            title = "Máy thắng"
            msg = "AI đã thắng ván này."
        else:
            result = "DRAW"
            title = "Hòa"
            msg = "Bàn cờ đầy, hai bên hòa."
        self.memory.update_after_game(self.ai_history, result)
        self.log(f"Kết thúc ván: {result}. AI đã cập nhật bộ nhớ học.")
        show_end_message(self.master, title, msg, self.restart)
        return True

    def restart(self):
        self.board.reset()
        self.game_over = False
        self.paused = False
        self.last_move = None
        self.move_history.clear()
        self.ai_history.clear()
        self.draw_board()
        self.log("--- Ván mới ---")

    def undo(self):
        if self.game_over or len(self.move_history) == 0:
            return
        # Undo last AI move and last human move so the player can choose another square.
        for _ in range(min(2, len(self.move_history))):
            r, c, p = self.move_history.pop()
            self.board.undo_move(r, c)
            if p == AI and self.ai_history:
                self.ai_history.pop()
        self.last_move = self.move_history[-1][:2] if self.move_history else None
        self.draw_board()
        self.log("Đã đi lại một lượt.")

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Tiếp tục" if self.paused else "Tạm dừng")
        self.log("Đã tạm dừng." if self.paused else "Tiếp tục ván chơi.")

    def clear_learning(self):
        if messagebox.askyesno("Xóa bộ nhớ", "Bạn chắc chắn muốn xóa dữ liệu học của AI?"):
            self.memory.clear()
            self.log("Đã xóa bộ nhớ học của AI.")
