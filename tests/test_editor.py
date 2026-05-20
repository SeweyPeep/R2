"""Tests for editor search behavior."""

import tkinter as tk

import pytest

from text_editor.editor import EditorPane


@pytest.fixture
def editor_widget() -> EditorPane:
    root = tk.Tk()
    root.withdraw()
    widget = EditorPane(root)
    yield widget
    widget.destroy()
    root.destroy()


def test_find_next_locates_query(editor_widget: EditorPane) -> None:
    editor_widget.load_content("alpha beta alpha")
    editor_widget.mark_set(tk.INSERT, "1.0")
    assert editor_widget.find_next("beta") is True
    assert editor_widget.get(tk.SEL_FIRST, tk.SEL_LAST) == "beta"


def test_find_next_returns_false_when_missing(editor_widget: EditorPane) -> None:
    editor_widget.load_content("hello")
    assert editor_widget.find_next("missing") is False


def test_cursor_position(editor_widget: EditorPane) -> None:
    editor_widget.load_content("ab\ncd")
    editor_widget.mark_set(tk.INSERT, "2.1")
    assert editor_widget.cursor_position() == (2, 2)
