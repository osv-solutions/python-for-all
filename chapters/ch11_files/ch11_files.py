"""Chapter 11: Files and Data Formats

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch11_files.py

or open the notebook and run the cells in order.
"""

# %% 11.1 Writing a text file
with open("shopping.txt", "w", encoding="utf-8") as f:
    f.write("milk\n")
    f.write("bread\n")
    f.write("eggs\n")
print("saved")

# %% 11.1 Writing a text file
with open("shopping.txt", "a", encoding="utf-8") as f:
    print("apples", file=f)
    print("rice", "2 kg", sep=", ", file=f)

# %% 11.2 Reading a text file
with open("shopping.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(number, line.rstrip("\n"))

# %% 11.2 Reading a text file
with open("shopping.txt", encoding="utf-8") as f:
    text = f.read()
print(repr(text[:20]))
lines = text.splitlines()
print(len(lines), "lines; last:", lines[-1])

# %% 11.2 Reading a text file
with open("cities.txt", "w", encoding="utf-8") as f:
    f.write("São Paulo\nZürich\nKraków\n")
with open("cities.txt", encoding="utf-8") as f:
    print(f.read().splitlines())

# %% 11.3 When files go wrong
# This example stops with an error on purpose (see the book).
try:
    with open("notes.txt", encoding="utf-8") as f:
        print(f.read())
except Exception:
    import traceback
    traceback.print_exc(limit=0)


# %% 11.3 When files go wrong
def load_lines(filename):
    """Return the lines of a text file, or [] if it doesn't exist."""
    try:
        with open(filename, encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []

print(load_lines("shopping.txt"))
print(load_lines("notes.txt"))

# %% 11.4 CSV files
import csv

rows = [["date", "item", "amount"],
        ["2026-10-01", "Groceries", 54.20],
        ["2026-10-02", "Bus pass", 30.00],
        ["2026-10-03", "Lunch, with Ravi", 18.75]]
with open("expenses.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
print(open("expenses.csv", encoding="utf-8").read(), end="")

# %% 11.4 CSV files
with open("expenses.csv", newline="", encoding="utf-8") as f:
    total = 0
    for row in csv.DictReader(f):
        amount = float(row["amount"])
        total += amount
        print(f"{row['date']}  {row['item']:<18}{amount:>7.2f}")
print(f"{'Total':<30}{total:>7.2f}")

# %% 11.4 CSV files
new = {"date": "2026-10-04", "item": "Book", "amount": 12.99}
with open("expenses.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "item", "amount"])
    writer.writerow(new)
print(open("expenses.csv", encoding="utf-8").read().splitlines()[-1])

# %% 11.5 JSON
import json

library = [
    {"title": "Dune", "year": 1965, "tags": ["sci-fi"], "read": True},
    {"title": "Emma", "year": 1815, "tags": [], "read": False},
]
text = json.dumps(library, indent=2)
print(text)

# %% 11.5 JSON
with open("library.json", "w", encoding="utf-8") as f:
    json.dump(library, f, indent=2)
with open("library.json", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded == library, type(loaded[0]))
print(loaded[0]["title"], loaded[0]["tags"])

# %% 11.6 Working with folders
from pathlib import Path

reports = Path("reports")
for region, sales in [("north", 120), ("south", 95), ("east", 143)]:
    folder = reports / region
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "sales.txt").write_text(f"{sales}\n", encoding="utf-8")
(reports / "README.txt").write_text("Weekly sales by region\n")

# %% 11.6 Working with folders
print(sorted(p.name for p in reports.iterdir()))
total = 0
for path in sorted(reports.rglob("sales.txt")):
    sales = int(path.read_text(encoding="utf-8"))
    total += sales
    print(f"{path.parent.name:<6}{sales:>5}")
print(f"{'total':<6}{total:>5}")

# %% 11.7 Putting it together: a reading log
import csv, json

LOG = "reading_log.csv"
FIELDS = ["title", "author", "pages"]

def load_log():
    try:
        with open(LOG, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

# %% 11.7 Putting it together: a reading log
def add_book(log, title, author, pages):
    log.append({"title": title, "author": author, "pages": pages})
    with open(LOG, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(log)

log = load_log()
new_books = [("Emma", "Jane Austen", 474),
             ("Persuasion", "Jane Austen", 249),
             ("Dune", "Frank Herbert", 688)]
for book in new_books:
    add_book(log, *book)
print(len(log), "books in the log")

# %% 11.7 Putting it together: a reading log
summary = {}
for book in load_log():
    totals = {"books": 0, "pages": 0}
    author = summary.setdefault(book["author"], totals)
    author["books"] += 1
    author["pages"] += int(book["pages"])
with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
print(open("authors.json", encoding="utf-8").read())
