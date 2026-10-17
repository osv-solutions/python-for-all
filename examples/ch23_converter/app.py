"""A unit converter: the mini project of Chapter 23 of Python for All.

Run it with: python app.py
"""
import tkinter as tk
from tkinter import ttk

from conversions import (CATEGORIES, convert, format_result,
                         parse_number, units)


class ConverterApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=16)
        self.category = tk.StringVar(value="Length")
        self.value = tk.StringVar(value="1")
        self.source = tk.StringVar()
        self.target = tk.StringVar()
        self.result = tk.StringVar()
        self.message = tk.StringVar()
        self.build_widgets()
        for var in (self.value, self.source, self.target):
            var.trace_add("write", self.update_result)
        self.choose_category()

    def add_row(self, row, text, widget):
        ttk.Label(self, text=text).grid(row=row, column=0, sticky="w",
                                        padx=(0, 8))
        widget.grid(row=row, column=1, sticky="ew", pady=4)
        return widget

    def build_widgets(self):
        category = self.add_row(0, "Quantity", ttk.Combobox(
            self, textvariable=self.category, values=CATEGORIES,
            state="readonly"))
        category.bind("<<ComboboxSelected>>", self.choose_category)
        entry = self.add_row(1, "Value",
                             ttk.Entry(self, textvariable=self.value))
        entry.bind("<Escape>", lambda event: self.value.set(""))
        entry.focus()
        self.source_box = self.add_row(2, "From", ttk.Combobox(
            self, textvariable=self.source, state="readonly"))
        self.target_box = self.add_row(3, "To", ttk.Combobox(
            self, textvariable=self.target, state="readonly"))
        ttk.Button(self, text="Swap", command=self.swap).grid(
            row=2, column=2, rowspan=2, sticky="ns", padx=(8, 0),
            pady=4)
        ttk.Label(self, textvariable=self.result,
                  font=("Segoe UI", 16, "bold")).grid(
            row=4, column=0, columnspan=3, pady=(12, 0))
        ttk.Label(self, textvariable=self.message,
                  foreground="firebrick").grid(row=5, column=0,
                                               columnspan=3)
        self.columnconfigure(1, weight=1)

    def choose_category(self, event=None):
        names = units(self.category.get())
        self.source_box["values"] = names
        self.target_box["values"] = names
        self.source.set(names[0])
        self.target.set(names[1])

    def swap(self):
        source, target = self.source.get(), self.target.get()
        self.source.set(target)
        self.target.set(source)

    def update_result(self, *args):
        try:
            number = parse_number(self.value.get())
            answer = convert(number, self.category.get(),
                             self.source.get(), self.target.get())
        except ValueError as err:
            self.result.set("")
            self.message.set(str(err))
        else:
            shown = format_result(answer)
            self.result.set(f"{shown} {self.target.get()}")
            self.message.set("")


def main():
    root = tk.Tk()
    root.title("Unit Converter")
    root.minsize(360, 0)
    ConverterApp(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
