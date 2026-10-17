"""Chapter 23: Desktop Apps with Tkinter

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch23_tkinter.py

or open the notebook and run the cells in order.
"""

# %% 23.2 Widgets and their options
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.withdraw()            # keep the window hidden in these examples
label = ttk.Label(root, text="Hello", padding=8)
print(label["text"])
label.config(text="Goodbye")
print(label.cget("text"))
print(label.winfo_class(), label)

# %% 23.4 Buttons and callbacks
def greet():
    print("Hello from the button!")

button = ttk.Button(root, text="Greet", command=greet)
button.invoke()
button.invoke()

# %% 23.4 Buttons and callbacks
def add(amount):
    print("adding", amount)

plus_one = ttk.Button(root, text="+1", command=lambda: add(1))
plus_ten = ttk.Button(root, text="+10", command=lambda: add(10))
plus_one.invoke()
plus_ten.invoke()

# %% 23.5 Control variables
name = tk.StringVar(value="Ada")
entry = ttk.Entry(root, textvariable=name)
print(entry.get())
name.set("Grace")
print(entry.get())
entry.delete(0, "end")
entry.insert(0, "Katherine")
print(name.get())

# %% 23.5 Control variables
count = tk.IntVar(value=41)
count.set(count.get() + 1)
print(count.get(), type(count.get()))

# %% 23.5 Control variables
def show_change(*args):
    print("name is now", name.get())

name.trace_add("write", show_change)
name.set("Ada")
entry.insert("end", " Lovelace")

# %% 23.5 Control variables
price = tk.DoubleVar()
price.set("twelve")
try:
    price.get()
except tk.TclError as err:
    print("TclError:", err)

# %% 23.8 Events and key bindings
def on_select(event):
    print("chose", event.widget.get())

sizes = ttk.Combobox(root, values=["small", "medium", "large"],
                     state="readonly")
sizes.bind("<<ComboboxSelected>>", on_select)
sizes.set("large")
sizes.event_generate("<<ComboboxSelected>>")

# %% 23.11 Timers with after
def tick(number):
    print("tick", number)
    if number < 3:
        root.after(100, tick, number + 1)
    else:
        root.quit()              # leave mainloop

root.after(100, tick, 1)
root.mainloop()
print("mainloop has returned")
