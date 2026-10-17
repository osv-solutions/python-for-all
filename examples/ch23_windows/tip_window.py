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


def calculate():
    try:
        tip, total, share = split_bill(float(bill.get()),
                                       float(percent.get()),
                                       int(people.get()))
    except ValueError:
        answer.set("Please check the numbers.")
        return
    answer.set(f"Tip ${tip:.2f}, each pays ${share:.2f}")


fields = [("Bill ($)", bill), ("Tip (%)", percent),
          ("People", people)]
for row, (text, variable) in enumerate(fields):
    ttk.Label(form, text=text).grid(row=row, column=0, sticky="w")
    ttk.Entry(form, textvariable=variable, width=12).grid(
        row=row, column=1, sticky="ew", padx=(8, 0), pady=3)
ttk.Button(form, text="Calculate", command=calculate).grid(
    row=3, column=0, columnspan=2, sticky="ew", pady=(8, 4))
ttk.Label(form, textvariable=answer).grid(row=4, column=0,
                                          columnspan=2)
form.columnconfigure(1, weight=1)
root.bind("<Return>", lambda event: calculate())
root.mainloop()
