import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Counter")
count = tk.IntVar(value=0)


def add_one():
    count.set(count.get() + 1)


def reset():
    count.set(0)


ttk.Label(root, textvariable=count,
          font=("Segoe UI", 28)).pack(padx=48, pady=(12, 4))
ttk.Button(root, text="Add one", command=add_one).pack(
    fill="x", padx=16)
ttk.Button(root, text="Reset", command=reset).pack(
    fill="x", padx=16, pady=(4, 16))
root.mainloop()
