import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Hello")
ttk.Label(root, text="Hello, Ada!", padding=24).pack()
ttk.Button(root, text="Quit", command=root.destroy).pack(pady=(0, 16))
root.mainloop()
