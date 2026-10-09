# Solutions: Chapter 11, Files and Data Formats

Worked solutions to the exercises at the end of Chapter 11 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch11_solutions.ipynb`](ch11_solutions.ipynb) or the script `ch11_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 11.1

*Write the numbers 1 to 10 and their squares to `squares.txt`, then read the file back and print the sum of the squares.*

```python
with open("squares.txt", "w", encoding="utf-8") as f:
    for n in range(1, 11):
        print(n, n * n, file=f)
total = 0
with open("squares.txt", encoding="utf-8") as f:
    for line in f:
        n, square = line.split()
        total += int(square)
print("Sum of the squares:", total)
```

Output:

```text
Sum of the squares: 385
```

`print(..., file=f)` writes each pair with a space between and a line break at the end. Reading back, `split()` separates the two numbers on each line, and only the square is added. The sum of the first ten squares is 385.

## Exercise 11.2

*Append the date and a message to `diary.txt` each time the program runs, then print the number of entries.*

A real diary would use `date.today()`. To make the output reproducible, this solution passes the date in and simulates three runs:

```python
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
```

Output:

```text
3 entries
2026-10-08  Started Part II
2026-10-09  Lists!
2026-10-10  Dictionaries make sense
```

Mode `"a"` adds to the end of the file, so the entries accumulate run after run. `readlines()` returns a list of the lines, whose length is the number of entries. `unlink(missing_ok=True)` deletes the file if it exists; it is here only so that the demonstration starts from an empty diary every time.

## Exercise 11.3

*Write `word_count(filename)` that returns the lines, words and characters of a file, or `None` if it doesn't exist.*

```python
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
```

Output:

```text
(3, 9, 48)
No such file: missing.txt
None
```

The file is read once, and the three counts come from the same text: `splitlines` for lines, `split` for words and `len` for characters, line breaks included. A missing file prints a message and returns `None` instead of crashing.

## Exercise 11.4

*Write a CSV file of five students, then print the class average and the students above it.*

```python
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
```

Output:

```text
Average: 75.6
Above: ['Asha', 'Chen', 'Eli']
```

The header row is written first, then the five students as tuples. Reading back with `DictReader` gives dictionaries whose values are all strings, so each score is converted with `int`. The average is 75.6, and Asha, Chen and Eli are above it. (The two list comprehensions are explained in Chapter 14; a loop with `append` does the same.)

## Exercise 11.5

*Save settings as JSON, load them, change the level and add a score, and save again.*

```python
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
```

Output:

```text
{"name": "Asha", "level": 3, "sound": true, "scores": [120, 95]}
{"name": "Asha", "level": 4, "sound": true, "scores": [120, 95, 140]}
```

Without `indent`, `json.dump` writes everything on one line, which is compact but harder to read. The loaded data is an ordinary dictionary, so the level is changed and the list of scores extended with the usual operations before saving again. `True` appears as `true` in the file.

## Exercise 11.6

*Convert `expenses.csv` to a JSON list of dictionaries, with the amounts stored as numbers.*

<details>
<summary>Setup code: recreates the data and helpers from the chapter (click to show)</summary>

```python
import csv
rows = [["date", "item", "amount"],
        ["2026-10-01", "Groceries", 54.20],
        ["2026-10-02", "Bus pass", 30.00],
        ["2026-10-03", "Lunch, with Ravi", 18.75]]
with open("expenses.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
```

</details>

```python
import csv, json

with open("expenses.csv", newline="", encoding="utf-8") as f:
    expenses = list(csv.DictReader(f))
for row in expenses:
    row["amount"] = float(row["amount"])
with open("expenses.json", "w", encoding="utf-8") as f:
    json.dump(expenses, f, indent=2)
print(open("expenses.json", encoding="utf-8").read())
```

Output:

```text
[
  {
    "date": "2026-10-01",
    "item": "Groceries",
    "amount": 54.2
  },
  {
    "date": "2026-10-02",
    "item": "Bus pass",
    "amount": 30.0
  },
  {
    "date": "2026-10-03",
    "item": "Lunch, with Ravi",
    "amount": 18.75
  }
]
```

The setup cell recreates the file from the chapter. Each row from `DictReader` is a dictionary of strings; converting the amount to a float before saving means that the JSON file stores a number, which any program reading the JSON can use directly.

## Exercise 11.7

*Report every `.txt` file in a folder and its subfolders with its number of lines and size, largest first, with a total.*

```python
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
```

Output:

```text
library/fiction/dune.txt    40 lines   240 chars
library/fiction/emma.txt    25 lines   225 chars
library/notes/todo.txt       3 lines    30 chars
total                       68 lines   495 chars
```

The first loop creates a small folder tree to report on. `rglob("*.txt")` finds the text files in every subfolder. Each file becomes a tuple that starts with its size, so `sorted(..., reverse=True)` puts the largest first. `str(path)` turns the path into text so that it can be padded to a fixed width.
