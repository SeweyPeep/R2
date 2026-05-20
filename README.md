# Tkinter Text Editor

A small Python text editor built with Tkinter. It is structured for learning, demos, and SonarQube static analysis in VS Code.

## Features

- New, open, save, and save-as
- Undo, redo, cut, copy, paste
- Find next match
- Word wrap toggle
- Status bar with line/column and modified indicator
- Unsaved-changes prompt on new, open, and exit

## Requirements

- Python 3.10+ (Tkinter is included with the standard library on Windows)

## Run the editor

```bash
python main.py
```

## Run tests

```bash
python -m pip install -r requirements-dev.txt
pytest
```

With coverage (useful before SonarQube):

```bash
pytest --cov=text_editor --cov-report=xml
```

## VS Code

Open this folder in VS Code and run `main.py` with the Python extension. No extra UI packages are required.

## SonarQube

1. Push this repository to GitHub.
2. Point SonarQube (or SonarCloud) at the repo.
3. Use `sonar-project.properties` in the project root, or map the same settings in your CI workflow.

Update `sonar.projectKey` in `sonar-project.properties` to match your SonarQube project key.
