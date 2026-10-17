import time
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Clock")
now = tk.StringVar()
ttk.Label(root, textvariable=now, font=("Consolas", 32),
          padding=(32, 16)).pack()


def tick():
    now.set(time.strftime("%H:%M:%S"))
    root.after(1000, tick)        # run again in 1000 ms


tick()
root.mainloop()
