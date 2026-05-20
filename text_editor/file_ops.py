"""File read/write helpers for the text editor."""

from pathlib import Path


def read_text_file(path: Path) -> str:
    """Read a text file and return its contents."""
    return path.read_text(encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    """Write content to a text file."""
    path.write_text(content, encoding="utf-8", newline="\n")


def display_name(path: Path | None) -> str:
    """Return a user-facing title for the current file."""
    if path is None:
        return "Untitled"
    return path.name
