import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Counter")
count = tk.IntVar(value=0)


def add_one():
    count.set(count.get() + 1)


def subtract_one():
    count.set(max(count.get() - 1, 0))


def reset():
    count.set(0)


ttk.Label(root, textvariable=count,
          font=("Segoe UI", 28)).pack(padx=48, pady=(12, 4))
for text, callback in [("Add one", add_one),
                       ("Subtract one", subtract_one),
                       ("Reset", reset)]:
    ttk.Button(root, text=text, command=callback).pack(
        fill="x", padx=16, pady=(0, 4))
root.mainloop()
