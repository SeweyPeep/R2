"""Main application window and menus."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from text_editor import __version__
from text_editor.dialogs import ask_save_changes, prompt_find_text, show_error, show_info
from text_editor.editor import EditorPane
from text_editor.file_ops import display_name, read_text_file, write_text_file

APP_TITLE = "Simple Text Editor"


class TextEditorApp:
    """Tkinter text editor with common file and edit actions."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.minsize(640, 420)
        self.root.geometry("900x600")

        self.current_path: Path | None = None
        self.modified = False
        self.word_wrap = True

        self.editor = EditorPane(self.root)
        self.editor.pack(fill=tk.BOTH, expand=True)
        self.editor.set_modified_callback(self._mark_modified)

        self.status_var = tk.StringVar(value=self._status_text())
        status = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor=tk.W,
            relief=tk.SUNKEN,
            padx=8,
        )
        status.pack(fill=tk.X, side=tk.BOTTOM)

        self._build_menu()
        self._bind_shortcuts()
        self.editor.bind("<KeyRelease>", lambda _e: self._refresh_status())
        self.editor.bind("<ButtonRelease>", lambda _e: self._refresh_status())
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self._update_title()

    def run(self) -> None:
        self.root.mainloop()

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Alt+F4", command=self.quit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self._edit_undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self._edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.editor.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.editor.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.editor.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", accelerator="Ctrl+F", command=self.find_text)
        edit_menu.add_command(label="Toggle Word Wrap", command=self.toggle_word_wrap)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def _bind_shortcuts(self) -> None:
        self.root.bind_all("<Control-n>", lambda _e: self.new_file())
        self.root.bind_all("<Control-o>", lambda _e: self.open_file())
        self.root.bind_all("<Control-s>", lambda _e: self.save_file())
        self.root.bind_all("<Control-S>", lambda _e: self.save_file_as())
        self.root.bind_all("<Control-f>", lambda _e: self.find_text())
        self.root.bind_all("<Control-z>", lambda _e: self._edit_undo())
        self.root.bind_all("<Control-y>", lambda _e: self._edit_redo())

    def _edit_undo(self) -> None:
        try:
            self.editor.edit_undo()
        except tk.TclError:
            pass

    def _edit_redo(self) -> None:
        try:
            self.editor.edit_redo()
        except tk.TclError:
            pass

    def _mark_modified(self) -> None:
        if not self.modified:
            self.modified = True
            self._update_title()
        self._refresh_status()

    def _status_text(self) -> str:
        line, column = self.editor.cursor_position()
        name = display_name(self.current_path)
        changed = " *" if self.modified else ""
        wrap = "wrap on" if self.word_wrap else "wrap off"
        return f"{name}{changed}  |  Line {line}, Col {column}  |  {wrap}"

    def _refresh_status(self) -> None:
        self.status_var.set(self._status_text())

    def _update_title(self) -> None:
        name = display_name(self.current_path)
        changed = "*" if self.modified else ""
        self.root.title(f"{name}{changed} - {APP_TITLE}")

    def _confirm_discard(self, action_title: str) -> bool:
        """Return True if it is safe to continue (saved or user discards)."""
        if not self.modified:
            return True
        choice = ask_save_changes(self.root, action_title)
        if choice is None:
            return False
        if choice:
            return self.save_file()
        return True

    def new_file(self) -> None:
        if not self._confirm_discard("New File"):
            return
        self.current_path = None
        self.modified = False
        self.editor.load_content("")
        self._update_title()
        self._refresh_status()

    def open_file(self) -> None:
        if not self._confirm_discard("Open File"):
            return
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Open File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        self._load_path(Path(path))

    def _load_path(self, path: Path) -> None:
        try:
            content = read_text_file(path)
        except OSError as exc:
            show_error(self.root, "Open Failed", str(exc))
            return
        self.current_path = path
        self.modified = False
        self.editor.load_content(content)
        self._update_title()
        self._refresh_status()

    def save_file(self) -> bool:
        if self.current_path is None:
            return self.save_file_as()
        return self._write_to_path(self.current_path)

    def save_file_as(self) -> bool:
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save As",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return False
        self.current_path = Path(path)
        return self._write_to_path(self.current_path)

    def _write_to_path(self, path: Path) -> bool:
        try:
            write_text_file(path, self.editor.get_all_text())
        except OSError as exc:
            show_error(self.root, "Save Failed", str(exc))
            return False
        self.modified = False
        self._update_title()
        self._refresh_status()
        return True

    def find_text(self) -> None:
        query = prompt_find_text(self.root)
        if query is None:
            return
        found = self.editor.find_next(query)
        if not found:
            show_info(self.root, "Find", f'No matches for "{query}".')
        self._refresh_status()

    def toggle_word_wrap(self) -> None:
        self.word_wrap = not self.word_wrap
        self.editor.configure(wrap="word" if self.word_wrap else "none")
        self._refresh_status()

    def show_about(self) -> None:
        show_info(
            self.root,
            "About",
            f"{APP_TITLE}\nVersion {__version__}\n\nA small Tkinter editor for learning and static analysis.",
        )

    def quit_app(self) -> None:
        if self._confirm_discard("Exit"):
            self.root.destroy()
