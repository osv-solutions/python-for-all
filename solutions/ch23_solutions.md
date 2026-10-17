# Solutions: Chapter 23, Desktop Apps with Tkinter

Worked solutions to the exercises at the end of Chapter 23 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch23_solutions.ipynb`](ch23_solutions.ipynb) or the script `ch23_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

The programs of these solutions are in `examples/ch23_solutions/` in the companion repository. Run each one with `python` and the file name; `python -m pytest` in that folder runs the tests of Exercises 5 and 6.

## Exercise 23.1

*Greet yourself by name, with a Quit button whose callback is the window's `destroy` method.*

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Hello")
ttk.Label(root, text="Hello, Ada!", padding=24).pack()
ttk.Button(root, text="Quit", command=root.destroy).pack(pady=(0, 16))
root.mainloop()
```

`command=root.destroy` passes the bound method without calling it, exactly like `command=self.add_one` in the chapter. When the button is clicked, `destroy` closes the window, `mainloop` returns, and the program ends. The label is never used again after `pack`, so it doesn't need a variable.

## Exercise 23.2

*Add a Subtract one button to the counter, never going below 0.*

```python
def subtract_one():
    count.set(max(count.get() - 1, 0))
```

`max(count.get() - 1, 0)` is 0 whenever the new value would be negative, so no `if` is needed. With three buttons, a loop over pairs of text and callback creates them with the same options:

```python
for text, callback in [("Add one", add_one),
                       ("Subtract one", subtract_one),
                       ("Reset", reset)]:
    ttk.Button(root, text=text, command=callback).pack(
        fill="x", padx=16, pady=(0, 4))
```

## Exercise 23.3

*Update the tip calculator as the user types, and use a `Spinbox` for the number of people.*

```python
ttk.Spinbox(form, textvariable=people, from_=1, to=20, width=10).grid(
    row=2, column=1, sticky="ew", padx=(8, 0), pady=3)
ttk.Label(form, textvariable=answer).grid(row=3, column=0,
                                          columnspan=2, pady=(8, 0))
form.columnconfigure(1, weight=1)
for variable in (bill, percent, people):
    variable.trace_add("write", calculate)
calculate()
root.mainloop()
```

`from_` has an underscore because `from` is a Python keyword. The spinbox shares the `StringVar` `people`, so clicking its arrows, or typing in it, writes the variable like typing in an entry. A trace on each of the three variables calls `calculate`, which now takes `*args` because a trace passes three values. The call before `mainloop` shows the answer for the starting values. While the user is halfway through typing, say `48.` or an empty box, `calculate` shows "Please check the numbers." for a moment, and the answer returns with the next keystroke.

## Exercise 23.4

*A word counter: a `Text` box and a label that counts words and characters as you type.*

The counting is a function of its own, which doesn't need a window:

```python
def describe(text):
    """Return a summary such as '2 words, 9 characters'."""
    words = len(text.split())
    return (f"{words} word{'' if words == 1 else 's'}, "
            f"{len(text)} characters")

print(describe(""))
print(describe("Hello"))
print(describe("Hello there,\n  Ada"))
```

Output:

```text
0 words, 0 characters
1 word, 5 characters
3 words, 18 characters
```

`split()` without an argument splits at any run of spaces, tabs and line breaks, so extra spaces don't count as words, while every character, spaces included, counts toward the length. The window connects it to the text box:

```python
def update(event=None):
    summary.set(describe(text.get("1.0", "end-1c")))


root = tk.Tk()
root.title("Word Counter")
text = tk.Text(root, width=50, height=10, wrap="word")
text.pack(padx=12, pady=(12, 4), fill="both", expand=True)
summary = tk.StringVar()
ttk.Label(root, textvariable=summary).pack(pady=(0, 12))
text.bind("<KeyRelease>", update)
text.focus()
update()
```

A `Text` widget numbers positions as `"line.column"`, so `"1.0"` is the start; `"end-1c"` is the end minus one character, the line break that a `Text` widget always keeps at its end. `<KeyRelease>` fires after the key has changed the text; with `<Key>`, which fires when the key goes down, the count would always be one keystroke behind. `wrap="word"` breaks long lines between words.

## Exercise 23.5

*Add Volume to the converter.*

Only `conversions.py` changes, in two places. The new units go into `FACTORS`, with the liter as the base unit:

```python
FACTORS = {
    "Length": {"millimeters": 0.001, "centimeters": 0.01, "meters": 1,
               "kilometers": 1000, "inches": 0.0254, "feet": 0.3048,
               "yards": 0.9144, "miles": 1609.344},
    "Weight": {"grams": 0.001, "kilograms": 1,
               "ounces": 0.028349523125, "pounds": 0.45359237,
               "stones": 6.35029318},
    "Volume": {"milliliters": 0.001, "liters": 1,
               "US cups": 0.2365882365, "US gallons": 3.785411784},
}
```

and the new quantity goes into the list the app shows:

```python
CATEGORIES = ["Length", "Weight", "Volume", "Temperature"]
```

`app.py` needs no change at all, because it never names a unit or a quantity: it shows `CATEGORIES`, asks `units` for the names, and passes everything to `convert`. That is the payoff of keeping the logic out of the window. The test checks a known conversion, 16 cups to a gallon:

```python
def test_volume():
    assert "Volume" in CATEGORIES
    assert units("Volume")[1] == "liters"
    assert convert(1, "Volume", "US gallons", "US cups") == (
        pytest.approx(16))
    assert convert(500, "Volume", "milliliters", "liters") == 0.5
```

## Exercise 23.6

*A to-do app with a `Listbox`, saved to JSON when the window closes.*

Loading and saving go in `todo_store.py`, which doesn't import `tkinter`:

```python
def load_tasks(path):
    """Return the saved tasks, or an empty list if there are none."""
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_tasks(path, tasks):
    Path(path).write_text(json.dumps(tasks, indent=2),
                          encoding="utf-8")
```

A third function, `add_task(tasks, title)`, strips the title and refuses a blank one, returning `True` only if it added the task. The window, `todo_app.py`, is a `ttk.Frame` subclass like the converter; its `path` parameter lets a test use a temporary file. These are its callbacks:

```python
    def show(self):
        self.listbox.delete(0, "end")
        for task in self.tasks:
            self.listbox.insert("end", task)

    def add(self):
        if add_task(self.tasks, self.new_task.get()):
            self.new_task.set("")
            self.show()

    def delete(self):
        for index in reversed(self.listbox.curselection()):
            del self.tasks[index]
        self.show()
```

The list `self.tasks` is the real data; `show` copies it into the listbox after every change. `curselection()` returns a tuple of selected positions. Deleting from the highest position down, with `reversed`, keeps the lower positions valid while items are removed. Saving happens when the window closes:

```python
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
```

`protocol("WM_DELETE_WINDOW", on_close)` replaces what the close button does: `on_close` calls `app.save()` and then `root.destroy()`, which the close button would otherwise have done by itself. The tests, in `test_todo.py`, save and load in `tmp_path` (Chapter 17), check that blank tasks are refused, and drive a hidden window: they add three tasks, select the second with `listbox.selection_set(1)`, delete it, and check the saved file.
