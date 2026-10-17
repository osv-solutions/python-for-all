import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Hello")
label = ttk.Label(root, text="Hello, Tkinter!", padding=24)
label.pack()
root.mainloop()
