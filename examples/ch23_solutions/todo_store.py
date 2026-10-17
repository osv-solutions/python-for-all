"""Load and save the to-do list: no tkinter here."""
import json
from pathlib import Path


def load_tasks(path):
    """Return the saved tasks, or an empty list if there are none."""
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_tasks(path, tasks):
    Path(path).write_text(json.dumps(tasks, indent=2),
                          encoding="utf-8")


def add_task(tasks, title):
    """Add a task unless it is blank; return True if it was added."""
    title = title.strip()
    if not title:
        return False
    tasks.append(title)
    return True
