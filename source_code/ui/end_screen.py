from __future__ import annotations
import tkinter as tk
from tkinter import messagebox

def show_end_message(root: tk.Tk, title: str, message: str, restart_callback):
    answer = messagebox.askyesno(title, message + "\n\nBạn có muốn chơi lại không?")
    if answer:
        restart_callback()
