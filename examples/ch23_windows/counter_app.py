import tkinter as tk
from tkinter import messagebox, ttk


class CounterApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self.count = tk.IntVar(value=0)
        ttk.Label(self, textvariable=self.count,
                  font=("Segoe UI", 28)).pack(pady=(0, 4))
        ttk.Button(self, text="Add one",
                   command=self.add_one).pack(fill="x")
        ttk.Button(self, text="Reset",
                   command=self.reset).pack(fill="x", pady=(4, 0))

    def add_one(self):
        self.count.set(self.count.get() + 1)

    def reset(self):
        if messagebox.askyesno("Reset", "Set the number back to 0?",
                               parent=self):
            self.count.set(0)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Counter")
    CounterApp(root).pack(fill="both", expand=True, padx=32)
    root.mainloop()
