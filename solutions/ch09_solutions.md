# Solutions: Chapter 9, Modules and the Standard Library

Worked solutions to the exercises at the end of Chapter 9 of *Python for All* by Vamsi Krishna Kandala. Try each exercise on your own first. Run the code yourself with the notebook [`ch09_solutions.ipynb`](ch09_solutions.ipynb) or the script `ch09_solutions.py`.

Numbers that depend on random data or library versions may differ slightly on your computer; the conclusions should not.

## Exercise 9.1

*Use `math` for the area of a circle of radius 5, the square root of 2, and the number of 12-egg boxes needed for 50 eggs.*

```python
import math

print(f"{math.pi * 5 ** 2:.2f}")
print(f"{math.sqrt(2):.5f}")
print(math.ceil(50 / 12))
```

Output:

```text
78.54
1.41421
5
```

The area of a circle is π*r*², 78.54 for a radius of 5. 50 eggs fill four boxes and leave two eggs over, which still need a box, so the answer is rounded *up* with `ceil`: 5 boxes.

## Exercise 9.2

*Print the mean, median and mode of some ages, and explain why the mean and the median differ.*

```python
import statistics

ages = [23, 31, 23, 45, 52, 23, 31, 38]
print(statistics.mean(ages), statistics.median(ages), statistics.mode(ages))
```

Output:

```text
33.25 31.0 23
```

The mean is 33.25, the median 31 and the mode 23. The median is the middle of the sorted ages (halfway between the fourth and fifth, 31 and 31). The mean is higher because the two oldest people, 45 and 52, pull it up; the median only cares about the order of the values, not how far the largest ones are from the middle.

## Exercise 9.3

*Ask for a birth date and print the weekday of birth and the age in days on December 31, 2026.*

```python
from datetime import date

born = date.fromisoformat(input("Birth date (YYYY-MM-DD): ").strip())
print("You were born on a", born.strftime("%A"))
days = (date(2026, 12, 31) - born).days
print(f"On 2026-12-31 you will be {days:,} days old.")
```

Output:

```text
Birth date (YYYY-MM-DD): 1990-05-17
You were born on a Thursday
On 2026-12-31 you will be 13,377 days old.
```

`fromisoformat` turns the text into a date (and raises a `ValueError` for anything else). Subtracting two dates gives a `timedelta`, whose `days` is the answer.

## Exercise 9.4

*Write `next_birthday(birth, today)` that returns the next birthday on or after today and the number of days until it.*

```python
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
```

Output:

```text
(datetime.date(2027, 5, 17), 221)
(datetime.date(2026, 12, 25), 78)
(datetime.date(2027, 3, 1), 144)
```

`replace(year=year)` gives the birthday in a given year. If it has already passed, the loop tries the next year. A birthday on February 29 doesn't exist in most years, so `replace` raises a `ValueError`, and this function then uses March 1, one common convention. May 17 has passed in 2026, so that birthday is in 2027, 221 days away; Christmas is still 78 days ahead.

## Exercise 9.5

*Draw a 7-card hand from a 52-card deck with `random.sample` and `random.seed(2)`.*

```python
import random

deck = []
for rank in "A23456789TJQK":
    for suit in "SHDC":
        deck.append(rank + suit)
random.seed(2)
hand = random.sample(deck, 7)
print(len(deck), "cards; hand:", " ".join(hand))
```

Output:

```text
52 cards; hand: AC 2H KD 6C 3D JD 5C
```

The nested loops build the 52 cards from 13 ranks and 4 suits, for example `"QH"` for the queen of hearts. `sample` picks seven *different* cards, just as a real deal can't give the same card twice.

## Exercise 9.6

*Create a folder with three text files, then print the name and size of each `.txt` file.*

```python
from pathlib import Path

folder = Path("practice")
folder.mkdir(exist_ok=True)
texts = {"a.txt": "Hello\n", "b.txt": "Python for All\n", "c.txt": "x" * 100}
for name, text in texts.items():
    (folder / name).write_text(text, encoding="utf-8")
for path in sorted(folder.glob("*.txt")):
    print(path.name, len(path.read_text(encoding="utf-8")))
```

Output:

```text
a.txt 6
b.txt 15
c.txt 100
```

The size is measured in characters by reading the file and taking the length of the text. `path.stat().st_size` gives the size in bytes instead, which is the same for plain English text but larger for accented letters and other non-English characters in UTF-8.

## Exercise 9.7

*Turn `next_birthday` into a module `birthdays.py` and import it from a second program.*

The module file holds the function from exercise 9.4, a docstring and a demonstration that runs only when the file itself is run:

```python
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
```

This cell writes the module to disk so that the solution can run as a whole; normally you would type it into `birthdays.py` in your editor. The second program imports it. Importing doesn't run the demonstration, because `__name__` is then `"birthdays"`:

```python
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
```

Output:

```text
Ravi  20 Oct  in 12 days
Mei   02 Dec  in 55 days
Asha  14 Mar  in 157 days
```

Each friend's next birthday is stored as a tuple that starts with the number of days, so sorting the tuples puts the soonest birthday first: Ravi in 12 days.
