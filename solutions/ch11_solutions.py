"""Solutions to the Chapter 11 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch11_solutions.py

The explanations are in ch11_solutions.md."""

# %% Exercise 11.1
with open("squares.txt", "w", encoding="utf-8") as f:
    for n in range(1, 11):
        print(n, n * n, file=f)
total = 0
with open("squares.txt", encoding="utf-8") as f:
    for line in f:
        n, square = line.split()
        total += int(square)
print("Sum of the squares:", total)

# %% Exercise 11.2
from datetime import date
from pathlib import Path

def write_entry(message, when):
    with open("diary.txt", "a", encoding="utf-8") as f:
        f.write(f"{when.isoformat()}  {message}\n")
    with open("diary.txt", encoding="utf-8") as f:
        return len(f.readlines())

Path("diary.txt").unlink(missing_ok=True)   # start fresh for the demo
for day, message in [(8, "Started Part II"), (9, "Lists!"),
                     (10, "Dictionaries make sense")]:
    count = write_entry(message, date(2026, 10, day))
print(count, "entries")
print(Path("diary.txt").read_text(encoding="utf-8"), end="")

# %% Exercise 11.3
def word_count(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"No such file: {filename}")
        return None
    return len(text.splitlines()), len(text.split()), len(text)

with open("poem.txt", "w", encoding="utf-8") as f:
    f.write("Roses are red,\nViolets are blue,\nPython is fun.\n")
print(word_count("poem.txt"))
print(word_count("missing.txt"))

# %% Exercise 11.4
import csv

students = [("Asha", 88), ("Ben", 52), ("Chen", 92),
            ("Dina", 67), ("Eli", 79)]
with open("scores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "score"])
    writer.writerows(students)
with open("scores.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
scores = [int(row["score"]) for row in rows]
average = sum(scores) / len(scores)
print(f"Average: {average:.1f}")
print("Above:", [row["name"] for row in rows if int(row["score"]) > average])

# %% Exercise 11.5
import json

settings = {"name": "Asha", "level": 3, "sound": True, "scores": [120, 95]}
with open("settings.json", "w", encoding="utf-8") as f:
    json.dump(settings, f)
print(open("settings.json", encoding="utf-8").read())
with open("settings.json", encoding="utf-8") as f:
    loaded = json.load(f)
loaded["level"] += 1
loaded["scores"].append(140)
with open("settings.json", "w", encoding="utf-8") as f:
    json.dump(loaded, f)
print(open("settings.json", encoding="utf-8").read())

# %% Exercise 11.6
# Setup: recreates the context these solutions build on (from the chapter).
import csv
rows = [["date", "item", "amount"],
        ["2026-10-01", "Groceries", 54.20],
        ["2026-10-02", "Bus pass", 30.00],
        ["2026-10-03", "Lunch, with Ravi", 18.75]]
with open("expenses.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

# %% Exercise 11.6
import csv, json

with open("expenses.csv", newline="", encoding="utf-8") as f:
    expenses = list(csv.DictReader(f))
for row in expenses:
    row["amount"] = float(row["amount"])
with open("expenses.json", "w", encoding="utf-8") as f:
    json.dump(expenses, f, indent=2)
print(open("expenses.json", encoding="utf-8").read())

# %% Exercise 11.7
from pathlib import Path

root = Path("library")
for sub, name, text in [("fiction", "dune.txt", "Spice\n" * 40),
                        ("fiction", "emma.txt", "Highbury\n" * 25),
                        ("notes", "todo.txt", "Read more\n" * 3)]:
    (root / sub).mkdir(parents=True, exist_ok=True)
    (root / sub / name).write_text(text, encoding="utf-8")
report = []
for path in root.rglob("*.txt"):
    text = path.read_text(encoding="utf-8")
    report.append((len(text), len(text.splitlines()), path))
for size, lines, path in sorted(report, reverse=True):
    print(f"{str(path):<26}{lines:>4} lines{size:>6} chars")
print(f"{'total':<26}{sum(r[1] for r in report):>4} lines"
      f"{sum(r[0] for r in report):>6} chars")
