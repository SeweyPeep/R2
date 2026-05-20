"""Entry point for the Tkinter text editor."""

from text_editor.app import TextEditorApp


def main() -> None:
    app = TextEditorApp()
    app.run()


if __name__ == "__main__":
    main()
