"""Editor widget and text search utilities."""

import tkinter as tk
from tkinter import scrolledtext


class EditorPane(scrolledtext.ScrolledText):
    """Main editing area with undo support."""

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(
            master,
            undo=True,
            maxundo=-1,
            wrap="word",
            font=("Consolas", 11),
            tabs="2c",
            **kwargs,
        )
        self.bind("<<Modified>>", self._on_modified_flag)
        self._modified_callback = None

    def set_modified_callback(self, callback) -> None:
        self._modified_callback = callback

    def _on_modified_flag(self, _event=None) -> None:
        if self._modified_callback is not None:
            self._modified_callback()
        self.edit_modified(False)

    def clear(self) -> None:
        self.delete("1.0", tk.END)
        self.edit_reset()
        self.edit_modified(False)

    def load_content(self, content: str) -> None:
        self.clear()
        self.insert("1.0", content)
        self.edit_modified(False)

    def get_all_text(self) -> str:
        return self.get("1.0", "end-1c")

    def cursor_position(self) -> tuple[int, int]:
        """Return 1-based line and column for the insert cursor."""
        index = self.index(tk.INSERT)
        line, column = index.split(".")
        return int(line), int(column) + 1

    def find_next(self, query: str, case_sensitive: bool = False) -> bool:
        """Select the next occurrence of query. Returns True if found."""
        if not query:
            return False

        start = self.index(tk.INSERT)
        if self.tag_ranges(tk.SEL):
            start = self.index(tk.SEL + "+1c")

        flags = [] if case_sensitive else ["-nocase"]
        pos = self.search(query, start, stopindex=tk.END, *flags)
        if not pos:
            pos = self.search(query, "1.0", stopindex=start, *flags)
        if not pos:
            return False

        end = f"{pos}+{len(query)}c"
        self.tag_remove(tk.SEL, "1.0", tk.END)
        self.tag_add(tk.SEL, pos, end)
        self.mark_set(tk.INSERT, end)
        self.see(pos)
        return True
