import tkinter as tk
from tkinter import ttk

from todo_store import add_task, load_tasks, save_tasks

TASKS_FILE = "tasks.json"


class TodoApp(ttk.Frame):
    def __init__(self, master, path=TASKS_FILE):
        super().__init__(master, padding=12)
        self.path = path
        self.tasks = load_tasks(path)
        self.new_task = tk.StringVar()
        entry = ttk.Entry(self, textvariable=self.new_task)
        entry.grid(row=0, column=0, sticky="ew")
        entry.bind("<Return>", lambda event: self.add())
        entry.focus()
        ttk.Button(self, text="Add", command=self.add).grid(
            row=0, column=1, padx=(8, 0))
        self.listbox = tk.Listbox(self, height=10)
        self.listbox.grid(row=1, column=0, columnspan=2, sticky="nsew",
                          pady=8)
        ttk.Button(self, text="Delete", command=self.delete).grid(
            row=2, column=0, columnspan=2, sticky="e")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.show()

    def show(self):
        self.listbox.delete(0, "end")
        for task in self.tasks:
            self.listbox.insert("end", task)

    def add(self):
        if add_task(self.tasks, self.new_task.get()):
            self.new_task.set("")
            self.show()

    def delete(self):
        for index in reversed(self.listbox.curselection()):
            del self.tasks[index]
        self.show()

    def save(self):
        save_tasks(self.path, self.tasks)


def main():
    root = tk.Tk()
    root.title("To-Do")
    app = TodoApp(root)
    app.pack(fill="both", expand=True)

    def on_close():
        app.save()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
