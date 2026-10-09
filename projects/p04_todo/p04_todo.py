"""Project 4 (Beginner): To-Do List Manager that Saves to JSON

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python p04_todo.py

The script asks you to type answers. To replay the answers used
in the book instead:

    python p04_todo.py < p04_todo.inputs.txt

You can also open the notebook and run the cells in order.
"""

# %% Step 1: Design the data
import json
from datetime import date

FILENAME = "todo.json"
TODAY = date(2026, 10, 8)   # use date.today() in a real program

# %% Step 1: Design the data
# Setup: recreates the context this solution builds on (not printed in the book).
from pathlib import Path
Path(FILENAME).unlink(missing_ok=True)   # start each run of the examples afresh

# %% Step 2: Load and save
def load_tasks():
    """Return the saved tasks, or [] if there are none yet."""
    try:
        with open(FILENAME, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Warning: {FILENAME} is damaged; starting empty.")
        return []

def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

# %% Step 2: Load and save
save_tasks([{"title": "Test", "due": None, "done": False}])
print(load_tasks())
save_tasks([])

# %% Step 3: Adding tasks
def add_task(tasks, title, due=None):
    """Add a task; due is a "YYYY-MM-DD" string or None."""
    title = title.strip()
    if not title:
        raise ValueError("a task needs a title")
    if due:
        due = date.fromisoformat(due).isoformat()
    tasks.append({"title": title, "due": due, "done": False})

tasks = load_tasks()
add_task(tasks, "Pay rent", "2026-10-05")
add_task(tasks, "Buy a birthday card", "2026-10-12")
add_task(tasks, "Learn Python", None)
print(len(tasks), "tasks")

# %% Step 4: Listing tasks, urgent first
def urgency(task):
    """Sort key: open tasks first, then by due date, undated last."""
    return (task["done"], task["due"] or "9999-12-31")

def show_tasks(tasks):
    if not tasks:
        print("Nothing to do!")
    for number, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        due = task["due"] or ""
        late = ""
        if due and not task["done"] and due < TODAY.isoformat():
            late = "  OVERDUE"
        print(f"{number:>2}. [{mark}] {task['title']:<22}{due}{late}")

# %% Step 4: Listing tasks, urgent first
tasks.sort(key=urgency)
show_tasks(tasks)

# %% Step 5: Completing and removing tasks
def pick(tasks, text):
    """Return the index of the task numbered text (1-based)."""
    if not text.strip().isdigit():
        raise ValueError(f"{text!r} is not a task number")
    index = int(text) - 1
    if not 0 <= index < len(tasks):
        raise ValueError(f"there is no task {text.strip()}")
    return index

def complete(tasks, text):
    tasks[pick(tasks, text)]["done"] = True

def remove(tasks, text):
    return tasks.pop(pick(tasks, text))

# %% Step 6: The command loop
def run_command(tasks, line):
    """Carry out one command; raise ValueError for bad input."""
    command, _, rest = line.partition(" ")
    match command:
        case "add":
            title, _, due = rest.partition("@")
            add_task(tasks, title, due.strip() or None)
        case "done":
            complete(tasks, rest)
        case "remove":
            print("Removed:", remove(tasks, rest)["title"])
        case "list":
            pass
        case _:
            raise ValueError("try add, done, remove, list or quit")

# %% Step 6: The command loop
def main():
    tasks = load_tasks()
    while (line := input("todo> ").strip()) != "quit":
        try:
            run_command(tasks, line)
        except ValueError as err:
            print("  Sorry:", err)
            continue
        tasks.sort(key=urgency)
        save_tasks(tasks)
        show_tasks(tasks)

# %% Step 6: The command loop
save_tasks(tasks)
main()

# %% Step 6: The command loop
main()
