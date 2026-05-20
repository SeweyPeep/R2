"""Simple dialog helpers."""

import tkinter as tk
from tkinter import messagebox, simpledialog


def ask_save_changes(parent: tk.Misc, title: str) -> bool | None:
    """Ask whether to save unsaved changes. Returns True/False/None (cancel)."""
    return messagebox.askyesnocancel(
        title,
        "Do you want to save your changes?",
        parent=parent,
        icon=messagebox.WARNING,
    )


def show_error(parent: tk.Misc, title: str, message: str) -> None:
    messagebox.showerror(title, message, parent=parent)


def show_info(parent: tk.Misc, title: str, message: str) -> None:
    messagebox.showinfo(title, message, parent=parent)


def prompt_find_text(parent: tk.Misc) -> str | None:
    value = simpledialog.askstring("Find", "Search for:", parent=parent)
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None
