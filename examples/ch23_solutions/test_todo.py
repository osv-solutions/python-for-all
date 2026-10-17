import tkinter as tk

import pytest

from todo_app import TodoApp
from todo_store import add_task, load_tasks, save_tasks


def test_save_and_load(tmp_path):
    path = tmp_path / "tasks.json"
    assert load_tasks(path) == []
    save_tasks(path, ["Buy milk", "Call Ada"])
    assert load_tasks(path) == ["Buy milk", "Call Ada"]


def test_blank_tasks_are_not_added():
    tasks = []
    assert add_task(tasks, "  Buy milk ")
    assert not add_task(tasks, "   ")
    assert tasks == ["Buy milk"]


def test_the_window_adds_and_deletes(tmp_path):
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display to create a window on")
    root.withdraw()
    app = TodoApp(root, tmp_path / "tasks.json")
    for title in ["Buy milk", "Call Ada", "Water plants"]:
        app.new_task.set(title)
        app.add()
    app.listbox.selection_set(1)
    app.delete()
    app.save()
    root.destroy()
    assert load_tasks(tmp_path / "tasks.json") == ["Buy milk",
                                                   "Water plants"]
