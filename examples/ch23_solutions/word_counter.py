import tkinter as tk
from tkinter import ttk


def describe(text):
    """Return a summary such as '2 words, 9 characters'."""
    words = len(text.split())
    return (f"{words} word{'' if words == 1 else 's'}, "
            f"{len(text)} characters")


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

if __name__ == "__main__":
    root.mainloop()
