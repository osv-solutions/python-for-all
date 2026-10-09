"""Solutions to the Chapter 9 exercises

Companion code for "Python for All"
by Vamsi Krishna Kandala. Run it from this folder:

    python ch09_solutions.py

The explanations are in ch09_solutions.md."""

# %% Exercise 9.1
import math

print(f"{math.pi * 5 ** 2:.2f}")
print(f"{math.sqrt(2):.5f}")
print(math.ceil(50 / 12))

# %% Exercise 9.2
import statistics

ages = [23, 31, 23, 45, 52, 23, 31, 38]
print(statistics.mean(ages), statistics.median(ages), statistics.mode(ages))

# %% Exercise 9.3
from datetime import date

born = date.fromisoformat(input("Birth date (YYYY-MM-DD): ").strip())
print("You were born on a", born.strftime("%A"))
days = (date(2026, 12, 31) - born).days
print(f"On 2026-12-31 you will be {days:,} days old.")

# %% Exercise 9.4
from datetime import date

def next_birthday(birth, today):
    """Return (date of next birthday, days until it)."""
    year = today.year
    while True:
        try:
            candidate = birth.replace(year=year)
        except ValueError:          # February 29 in a non-leap year
            candidate = date(year, 3, 1)
        if candidate >= today:
            return candidate, (candidate - today).days
        year += 1

today = date(2026, 10, 8)
print(next_birthday(date(1990, 5, 17), today))
print(next_birthday(date(1985, 12, 25), today))
print(next_birthday(date(2000, 2, 29), today))

# %% Exercise 9.5
import random

deck = []
for rank in "A23456789TJQK":
    for suit in "SHDC":
        deck.append(rank + suit)
random.seed(2)
hand = random.sample(deck, 7)
print(len(deck), "cards; hand:", " ".join(hand))

# %% Exercise 9.6
from pathlib import Path

folder = Path("practice")
folder.mkdir(exist_ok=True)
texts = {"a.txt": "Hello\n", "b.txt": "Python for All\n", "c.txt": "x" * 100}
for name, text in texts.items():
    (folder / name).write_text(text, encoding="utf-8")
for path in sorted(folder.glob("*.txt")):
    print(path.name, len(path.read_text(encoding="utf-8")))

# %% Exercise 9.7
from pathlib import Path

Path("birthdays.py").write_text('''"""Birthday helpers."""
from datetime import date


def next_birthday(birth, today):
    """Return (date of next birthday, days until it)."""
    year = today.year
    while True:
        try:
            candidate = birth.replace(year=year)
        except ValueError:
            candidate = date(year, 3, 1)
        if candidate >= today:
            return candidate, (candidate - today).days
        year += 1


if __name__ == "__main__":
    print(next_birthday(date(2000, 1, 1), date(2026, 10, 8)))
''', encoding="utf-8")

# %% Exercise 9.7
import birthdays
from datetime import date

friends = {"Asha": date(1992, 3, 14), "Ravi": date(1988, 10, 20),
           "Mei": date(1995, 12, 2)}
today = date(2026, 10, 8)
upcoming = []
for name, born in friends.items():
    when, days = birthdays.next_birthday(born, today)
    upcoming.append((days, name, when))
for days, name, when in sorted(upcoming):
    print(f"{name:<5} {when:%d %b}  in {days} days")
