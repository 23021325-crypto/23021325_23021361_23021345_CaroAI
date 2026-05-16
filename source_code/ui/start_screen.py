from __future__ import annotations
import tkinter as tk
from ui.game_screen import GameScreen

class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#edf2f4")
        self.master = master
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        box = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        box.place(relx=0.5, rely=0.5, anchor="center", width=520, height=340)
        tk.Label(box, text="GAME CARO AI", font=("Arial", 26, "bold"), fg="#023047", bg="#ffffff").pack(pady=(35, 8))
        tk.Label(box, text="Minimax - Alpha-Beta - Học kinh nghiệm", font=("Arial", 12), bg="#ffffff").pack(pady=4)
        tk.Label(box, text="Nhập tên người chơi", font=("Arial", 11, "bold"), bg="#ffffff").pack(pady=(28, 4))
        self.name_entry = tk.Entry(box, font=("Arial", 13), justify="center")
        self.name_entry.insert(0, "Người chơi")
        self.name_entry.pack(ipadx=40, ipady=6)
        tk.Button(box, text="Bắt đầu", command=self.start_game, font=("Arial", 13, "bold"), bg="#8ecae6", width=18).pack(pady=24)
        tk.Label(box, text="Luật: bàn cờ 9x9, ai có 4 quân liên tiếp trước sẽ thắng.", font=("Arial", 9), bg="#ffffff").pack()

    def start_game(self):
        name = self.name_entry.get().strip() or "Người chơi"
        self.destroy()
        GameScreen(self.master, name, back_callback=self.back_to_start).pack(fill="both", expand=True)

    def back_to_start(self):
        for child in self.master.winfo_children():
            child.destroy()
        StartScreen(self.master)
