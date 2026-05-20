"""Tests for file helper functions."""

from pathlib import Path

from text_editor.file_ops import display_name, read_text_file, write_text_file


def test_display_name_untitled() -> None:
    assert display_name(None) == "Untitled"


def test_display_name_with_path(tmp_path: Path) -> None:
    file_path = tmp_path / "notes.txt"
    assert display_name(file_path) == "notes.txt"


def test_write_and_read_round_trip(tmp_path: Path) -> None:
    target = tmp_path / "sample.txt"
    write_text_file(target, "hello\nworld")
    assert read_text_file(target) == "hello\nworld"
