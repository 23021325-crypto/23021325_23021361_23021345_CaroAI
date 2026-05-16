from __future__ import annotations
import tkinter as tk
from ui.start_screen import StartScreen

class CaroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caro AI - Minimax va Alpha-Beta")
        self.geometry("980x680")
        self.minsize(940, 650)
        StartScreen(self)

def run_app():
    app = CaroApp()
    app.mainloop()
