import tkinter as tk
from tkinter import ttk


def split_bill(bill, tip_percent, people):
    """Return the tip, the total and each person's share."""
    if people < 1:
        raise ValueError("people must be at least 1")
    tip = bill * tip_percent / 100
    total = bill + tip
    return tip, total, total / people


root = tk.Tk()
root.title("Tip Calculator")
form = ttk.Frame(root, padding=16)
form.pack(fill="both", expand=True)
bill = tk.StringVar(value="48.50")
percent = tk.StringVar(value="15")
people = tk.StringVar(value="2")
answer = tk.StringVar()


def calculate(*args):
    try:
        tip, total, share = split_bill(float(bill.get()),
                                       float(percent.get()),
                                       int(people.get()))
    except ValueError:
        answer.set("Please check the numbers.")
        return
    answer.set(f"Tip ${tip:.2f}, each pays ${share:.2f}")


ttk.Label(form, text="Bill ($)").grid(row=0, column=0, sticky="w")
ttk.Entry(form, textvariable=bill, width=12).grid(
    row=0, column=1, sticky="ew", padx=(8, 0), pady=3)
ttk.Label(form, text="Tip (%)").grid(row=1, column=0, sticky="w")
ttk.Entry(form, textvariable=percent, width=12).grid(
    row=1, column=1, sticky="ew", padx=(8, 0), pady=3)
ttk.Label(form, text="People").grid(row=2, column=0, sticky="w")
ttk.Spinbox(form, textvariable=people, from_=1, to=20, width=10).grid(
    row=2, column=1, sticky="ew", padx=(8, 0), pady=3)
ttk.Label(form, textvariable=answer).grid(row=3, column=0,
                                          columnspan=2, pady=(8, 0))
form.columnconfigure(1, weight=1)
for variable in (bill, percent, people):
    variable.trace_add("write", calculate)
calculate()
root.mainloop()
